import glob
import os
import plistlib
import re
import shutil
import sys
from argparse import ArgumentParser, Namespace
from itertools import filterfalse, groupby
from typing import List, Dict

import cairosvg
from PyPDF2.pdf import PdfFileReader

templates_dir = 'templates'
data_template_file = os.path.join(templates_dir, 'data.plist')
sheet_template_file = os.path.join(templates_dir, 'sheet.plist')
image_template_file = os.path.join(templates_dir, 'image.plist')


def main():
    args = parse_arguments()

    create_output_dir(args.stencil_file)

    image_pl_tpl = load_image_plist_template()
    images = list_images(args.svg_dir, args.filename_includes, args.filename_excludes)

    if not images:
        print('No SVG images found', file=sys.stderr)
        exit(1)

    grouped_images = group_images_by_dir(images)

    data_pl = create_data_plist()

    image_idx = 0
    for group_name, group_images in grouped_images.items():
        print(f'Processing {len(group_images)} images from group "{group_name}"')

        sheet_pl = create_sheet_plist(group_name)

        for svg_path in group_images:
            image_idx += 1
            pdf_image_path = save_image_as_pdf(svg_path, args.stencil_file, image_idx)
            stencil_name = create_stencil_name(svg_path, args.stencil_name_remove)
            add_image_to_sheet(sheet_pl, create_image_plist(pdf_image_path, image_pl_tpl, image_idx, stencil_name))

        add_sheet_to_data(data_pl, sheet_pl)

    save_data_plist(args.stencil_file, data_pl, args.text_output)

    print('Stencil created')


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description='Convert SVG files into OmniGraffle stencil')
    parser.add_argument('--svg-dir', default='./svg', help='svg files directory path (default: ./svg)')
    parser.add_argument('--stencil-file', default='output.gstencil',
                        help='name of output stencil file (default: output.gstencil)')
    parser.add_argument('--filename-includes', default=[], action='extend', nargs='*', type=str,
                        help='strings to filter image file name by, taking only those which contains them all')
    parser.add_argument('--filename-excludes', default=[], action='extend', nargs='*', type=str,
                        help='strings to filter image file name by, taking only those which do not contain any of them')
    parser.add_argument('--stencil-name-remove', default=['.', '-', '_'], action='extend', nargs='*', type=str,
                        help='strings to be removed from image file name when creating stencil name (default: . - _)')
    parser.add_argument('--text-output', default=False, action='store_true',
                        help='write OmniGraffle data file as text instead of binary')

    return parser.parse_args()


def create_output_dir(dir_name):
    shutil.rmtree(dir_name, ignore_errors=True)
    os.mkdir(dir_name)


def load_image_plist_template():
    return load_plist(image_template_file)


def list_images(dir_path: str, name_includes: List[str], name_excludes: List[str]) -> List[str]:
    files = [f for f in glob.glob(os.path.join(dir_path, '**/*.svg'))]

    files = filter_file_name_include(files, name_includes)
    files = filter_file_name_exclude(files, name_excludes)

    files.sort()

    return files


def filter_file_name_include(files: List[str], keywords: List[str]) -> List[str]:
    if not keywords:
        return files

    return list(
        filter(lambda file: all(keyword in os.path.basename(file) for keyword in keywords), files)
    )


def filter_file_name_exclude(files: List[str], keywords: List[str]) -> List[str]:
    if not keywords:
        return files

    return list(
        filterfalse(lambda file: any(keyword in os.path.basename(file) for keyword in keywords), files)
    )


def group_images_by_dir(images: List[str]) -> Dict[str, List[str]]:
    return {key: list(items) for key, items in groupby(images, lambda file_name: file_name.split('/')[-2])}


def create_data_plist():
    return load_plist(data_template_file)


def create_sheet_plist(sheet_title):
    sheet_pl = load_plist(sheet_template_file)
    sheet_pl['SheetTitle'] = sheet_title
    return sheet_pl


def add_sheet_to_data(data_pl, sheet_pl):
    images_count = len(sheet_pl['GraphicsList'])

    data_pl['Sheets'].append(sheet_pl)

    data_pl['ImageCounter'] += images_count
    data_pl['ImageList'].extend([f'image{image["ID"]}.pdf' for image in sheet_pl['GraphicsList']])


def create_image_plist(pdf_image_path, plist_template, idx, stencil_name):
    with open(pdf_image_path, 'rb') as fp:
        input1 = PdfFileReader(fp)
        media_box = input1.getPage(0).mediaBox

    image_pl = plist_template.copy()
    image_pl['Bounds'] = '{{0, 0}, {' + str(media_box[2]) + ', ' + str(media_box[3]) + '}}'
    image_pl['ID'] = idx
    image_pl['ImageID'] = idx
    image_pl['Name'] = stencil_name

    return image_pl


def add_image_to_sheet(sheet_pl, image_pls):
    sheet_pl['GraphicsList'].append(image_pls)


def save_image_as_pdf(source, dir_path, idx):
    pdf_path = os.path.join(dir_path, f'image{idx}.pdf')
    cairosvg.svg2pdf(url=source, write_to=pdf_path, dpi=72)
    return pdf_path


nonprintable = ''.join(c for c in map(chr, range(256)) if not c.isprintable())
nonprintable_translation_table = dict.fromkeys(map(ord, nonprintable), None)


def create_stencil_name(file_path, remove_from_stencil_name):
    name = os.path.splitext(os.path.basename(file_path))[0]

    name = re.sub(r'|'.join(map(re.escape, remove_from_stencil_name)), ' ', name)

    # filter out not printable characters, as they may be part of the badly generated file name
    # and will cause error when creating plist file
    name = name.translate(nonprintable_translation_table)

    name = re.sub(' +', ' ', name)

    name = name.strip()

    return name


def save_data_plist(path, data_pl, text_output: bool):
    data_file = os.path.join(path, 'data.plist')
    with open(data_file, 'wb') as fp:
        plistlib.dump(data_pl, fp)
        fmt = plistlib.FMT_XML if text_output else plistlib.FMT_BINARY
        # noinspection PyTypeChecker
        plistlib.dump(data_pl, fp, fmt=fmt)


def load_plist(file_path):
    with open(file_path, 'rb') as fp:
        return plistlib.load(fp)


if __name__ == '__main__':
    main()

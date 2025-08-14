import json
import re
from pathlib import Path
from datetime import datetime

with open('stone_db.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

output_dir = Path('archives')
output_dir.mkdir(exist_ok=True)

for feature in geojson_data.get('features', []):
    properties = feature.get('properties', {})
    geometry = feature.get('geometry', {})

    feature_id = properties.get('id')

    html_content = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="utf-8">'
    ]

    s_place = s_photo_date = s_built_year = s_built_year_ce = s_figure = s_principal = s_absence = ''
    lst_types = lst_images = lst_projects = lst_sameas = lst_comments = lst_ref_urls = lst_model_urls = lst_tags = []

    for key, value in properties.items():
        if key == 'contributor':
            s_contributor = value
        elif key == 'created_at':
            dt = datetime.strptime(value, '%Y-%m-%d')
            s_created_at = f'{dt.year}年{dt.month}月{dt.day}日'
        elif key == 'address':
            s_address = value
        elif key == 'place':
            s_place = value
        elif key == 'type':
            lst_types = value
        elif key == 'image':
            lst_images = value
        elif key == 'photo_date':
            try:
                dt = datetime.strptime(value, '%Y-%m-%d')
                s_photo_date = f'{dt.year}年{dt.month}月{dt.day}日'
            except:
                print(str(feature_id) + '：写真撮影日の日付形式が不正')
        elif key == 'city_code':
            s_city_code = str(value)
        elif key == 'built_year':
            s_built_year = value
        elif key == 'built_year_ce':
            s_built_year_ce = value
        elif key == 'figure':
            s_figure = value
        elif key == 'principal':
            s_principal = value
        elif key == 'project':
            lst_projects = value
        elif key == 'sameas':
            lst_sameas = value
        elif key == 'absence':
            s_absence = value;
        elif key == 'comment':
            lst_comments = value
        elif key == 'ref_url':
            lst_ref_urls = value
        elif key == '3D_model_url':
            lst_model_urls = value
        elif key == 'tag':
            lst_tags = value

    if s_place:
         s_address2 = s_address + ' ' + str(s_place)
    s_title = s_address2 + 'の' + ','.join(lst_types) + ' - みんなで石仏調査アーカイブ'
    html_content.append('<title>' + s_title + '</title>')

    html_content.extend([
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<link rel="stylesheet" href="css/bootstrap.min.css" type="text/css">',
        '<script src="js/bootstrap.bundle.min.js"></script>',
        '<script src="js/jquery-3.6.1.js"></script>',
        '<script>',
        'function popupImage(img){',
        'let html = \'<img src="images/\' + img + \'" style="width:100%;">\';',
        '$(\'#photo-popup-body\').html(html);',
        '$(\'#photo-popup\').modal(\'show\');',
        '}\r</script>',
        '</head>\r<body style="padding:10px;">',
        '<div id="photo-popup" class="modal fade hidden">',
        '<div class="modal-dialog modal-dialog-centered">',
        '<div class="modal-content">',
        '<div id="photo-popup-body" class="modal-body" data-bs-dismiss="modal">',
        '</div>\r</div>\r</div>\r</div>',
        '<p>みんなで石仏調査アーカイブ</p>\r<hr>',
    ])

    html_content.append('データ作成者：' + s_contributor + '<br>')
    html_content.append('データ作成日：' + s_created_at + '<br>')

    html_content.append('<div style="background-color:rgb(229 231 235);">')
    html_content.append('<table style="overflow-y:hidden;margin-right:10px"><tr>')
    for s_image in lst_images:
          html_content.append('<td><img src="images/' + s_image + '" ' +
                              'style="margin:5px;width:auto;height:200px;object-fit:contain;" ' +
                              'onClick="javascript:popupImage(\'' + s_image + '\');"></td>')
    html_content.append('</tr>\r</table>')
    html_content.append('<div style="margin-left:0.5rem;padding-bottom:0.5rem;">&copy;' + s_contributor + 
                        ' (Licensed under <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank">CC BY 4.0</a>)</div>\r</div>')
    if s_photo_date:
        html_content.append('写真撮影日：' + s_photo_date + '<br>')
    lst_coord = geometry.get('coordinates')
    html_content.append('緯度経度：' + str(lst_coord[1]) + ', ' + str(lst_coord[0]) + '<br>')
    html_content.append('所在地：' + s_address + '（' + s_city_code + '）<br>')
    if s_place:
        html_content.append('場所：' + str(s_place) + '<br>')
    if lst_types:
        html_content.append('種類：' + ','.join(lst_types) + '<br>')

    if s_built_year:
        html_content.append('造立年（和暦）：' + str(s_built_year) + '<br>')
    if s_built_year_ce:
        html_content.append('造立年（西暦）：' + str(s_built_year_ce) + '<br>')
    if s_figure:
        html_content.append('像容（刻像）：' + s_figure + '<br>')
    if s_principal:
        html_content.append('主尊銘：' + s_principal + '<br>')
    for s_project in lst_projects:
        html_content.append('プロジェクト：' + s_project + '<br>')
    for s_sameas in lst_sameas:
        html_content.append('同一物： <a href="' + str(s_sameas) + '.html">' + str(s_sameas) + '</a><br>')
    if s_absence == 'missing':
        html_content.append('不在種別：所在不明<br>');
    elif s_absence == 'moved':
        html_content.append('不在種別：移設<br>');
    for s_comment in lst_comments:
        html_content.append('備考：' + re.sub(r'\r\n|\r|\n', '<br>\r', s_comment) + '<br>')
    for s_ref_url in lst_ref_urls:
        html_content.append('参考URL：' + '<a href="' + s_ref_url + '" target="_blank">' + s_ref_url + '</a><br>')
    for s_model_url in lst_model_urls:
        html_content.append('3Dモデル：' + '<a href="' + s_model_url + '" target="_blank">' + s_model_url + '</a><br>')
    for s_tag in lst_tags:
        html_content.append('タグ：' + s_tag + '<br>');
    html_content.append('</body>\r</html>')

    file_path = output_dir / f"{feature_id}.html"
    with open(file_path, "w", encoding="utf-8") as html_file:
        html_file.write('\r'.join(html_content))

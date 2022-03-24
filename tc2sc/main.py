import os
from osgeo import ogr
import opencc

# 获取项目所在根目录
cws = os.getcwd()
ws = os.path.join(cws, 'tw')
# 将当前工作目录更改为指定路径
os.chdir(ws)

files = os.listdir(ws)
shp_files = []
for file in files:
    if file.endswith('.shp'):
        filename = file[0:file.find('.shp')]
        shp_files.append(filename)

# 注册驱动
driver = ogr.GetDriverByName('ESRI Shapefile')
shp_ds = driver.Open(ws, 1)  # 0为只读，1为可写

for shp_file in shp_files:
    # 获取图层
    buildings_lyr = shp_ds.GetLayer(shp_file)
    converter = opencc.OpenCC('t2s.json')  # t即traditional chinese;繁体，s即simplified chinese

    # 遍历所有要素
    buildings_lyr.ResetReading()  # 按顺序读取
    buildings_feature = buildings_lyr.GetNextFeature()
    while buildings_feature:
        name = buildings_feature.GetField('name')  # 获取name字段,若为空则name为None
        if name:  # 若不为空
            name = converter.convert(name)  # 若不为None则转为简体
            buildings_feature.SetField("name", name)  # 为字段设置新值
            # print(buildings_feature.GetField('name')) # 赋新值后再次读取看是否修改（写入）成功
            buildings_lyr.SetFeature(buildings_feature)
        # 清除缓存并获取下一个要素
        buildings_feature.Destroy()
        buildings_feature = buildings_lyr.GetNextFeature()
    print('{0}要素已被处理完毕'.format(shp_file))

print('所有要素均被处理完毕')
shp_ds.Destroy()  # 关闭数据源，结束读写

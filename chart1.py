from pyecharts.charts import Pie ,Grid,Bar,Line
from pyecharts.faker import Faker #数据包
from pyecharts.charts import Map,Geo
from pyecharts import options as opts
from pyecharts.globals import ThemeType

des1 = ['软件','大数据','人工智能','深度学习','机器学习','NLP','神经网络','目标检测','yolo','自动驾驶']
data1 = [48961,3844,3518,2023,3986,291,12878,1888,29,375]

c = (
    Bar()
    .add_xaxis(des1)
    .add_yaxis("博士以上论文总量", data1) #数据配置
    .set_global_opts(title_opts=opts.TitleOpts(title="Cnki爬取相关关键词论文整体统计", subtitle=" ")) #全局配置标题
)

c.render()
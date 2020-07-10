# BosonNER-Data-Pretreatment
bosonNER data pretreatment 玻森命名实体识别数据集的预处理，按照8:1:1进行训练集、验证集与测试集的切分，标注体系BMES

## 文件说明
1. python处理程序执行后，读取data文件夹下的boson数据，处理后在result文件夹生成BMES标注的训练集、验证集与测试集。
2. data文件夹中的数据为从boson官网下载的原始数据，只不过改了很少几处错误。想要查看标记错误，可以在代码第49行取消注释，使用原始boson数据查看输出。


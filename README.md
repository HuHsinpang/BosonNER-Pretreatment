# BosonNER-Data-Pretreatment
bosonNER data pretreatment 玻森命名实体识别数据集的预处理，按照8:1:1进行训练集、验证集与测试集的切分，标注体系BMES

## 文件说明
1. python处理程序执行后，读取data文件夹下的boson数据，处理后在result文件夹生成BMES标注的训练集、验证集与测试集。
2. data文件夹中的数据为从boson官网下载的原始数据，只不过改了很少几处错误。比如说“}}}}”括号的问题等等乱七八糟的，忘记记录了，数据内容无更改，只是改错。


基于多层异质网络的城市演化模型研究
==========
###摘要
  （待补充）
###代码说明
* _1_unpack.sh：
  * 对原始数据进行解压，以及启动后续代码，为了节省空间会对之前数据进行删除（如果没有抛出异常）
* _2_infoExtract.py:
  * 读取手机信令数据，去除不必要信息，仅保留通讯以及轨迹数据
* _3_gethome.py:
  * 依照轨迹数据计算每个用户的家的位置，即夜晚出现的最多的地方，去除出现次数在70次以下的
* _4_humanmobility.py:
  * 比较相邻月份的人口信息，获取新增人口、离开人口以及常驻人口


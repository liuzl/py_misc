# -*- encoding: utf-8 -*-

def nations_():
    for line in open("chinese_nations.txt"):
        line = line.strip()
        if len(line) > 2:
            yield line[:-1]
        yield line

nations = list(nations_())
nations.sort(reverse=True)

def province_names(name):
    if name.endswith('市'):
        return [name, name[:-1]]
    elif name.endswith('省'):
        return [name, name[:-1]]
    elif name == '内蒙古自治区':
        return [name, '内蒙古省', '内蒙古', '内蒙']
    elif name == '广西壮族自治区':
        return [name, '广西自治区', '广西省', '广西']
    elif name == '西藏自治区':
        return [name, '西藏省', '西藏']
    elif name == '新疆维吾尔自治区':
        return [name,'新疆维吾尔族自治区', '新疆自治区', '新疆省', '新疆']
    return [name]

def _zhou(name):
    x = name[:-3]
    for i in nations: x = x.replace(i,"")
    ret = [name,x+"自治州",x+"州",x+"市",x]
    if name == '克孜勒苏柯尔克孜自治州': ret.append("克州")
    elif name == '巴音郭楞蒙古自治州': ret.append("巴州")
    elif name == '博尔塔拉蒙古自治州': ret.append("博州")
    return ret

def city_names(name):
    if name.endswith('市'):
        ret = [name, name[:-1]]
        if name == '呼和浩特市': ret.append('呼市')
        return ret
    elif name.endswith('盟'):
        return [name, name[:-1]]
    elif name.endswith("自治州"):
        return _zhou(name)
    elif name.endswith("地区"):
        return [name, name[:-2]]
    return [name]

county_suffix = ['新区', '矿区','区', '县', '市', '现代产业园', '行政委员会', '管委会']
cnames = set(['市辖区', '山西转型综合改革示范区'])
def county_names(name):
    if len(name) <= 2 or name in cnames:
        return [name] # 赵县
    s = '高新技术产业开发区'
    if name.endswith(s):
        x = name[:-len(s)].rstrip('市')
        if len(x) <= 3 or x == '乌鲁木齐':
            return [name, s, '高新区']
        if x == '河北衡水':
            return [name, s, '高新区']
        if x == '包头稀土':
            return [name, '稀土'+s, '稀土高新区']
        if x == '长春净月':
            return [name, '净月'+s, '净月高新区', '净月']
        if x == '泰州医药':
            return [name, '医药'+s, '医药高新区']
        if x == '合肥新站':
            return [name, '新站'+s, '新站高新区']
        return [name]

    s = '高新技术产业园区'
    if name.endswith(s):
        return [name, s, '高新区']

    s = '工业园区'
    if name.endswith(s):
        if name == '呼和浩特金海工业园区':
            return [name, '金海工业园区', '金海', s, '工业园']
        if name =='格尔木藏青工业园区':
            return [name, '藏青工业园区', '藏青', s, '工业园']
        return [name, s, '工业园']
    
    if name == '石家庄循环化工园区':
        return [name, '循环化工园', '化工园']
    
    s = '管理区'
    if name.endswith(s):
        x = name[:-len(s)]
        if len(x) <= 3:
            return [name, x]
        x = x[x.find('市')+1:]
        return [name,x]
    
    s = '城乡一体化示范区'
    if name.endswith(s):
        return [name, '示范区']
    
    if name == '云龙示范区':
        return [name, '云龙', '示范区']
    if name == '湘潭昭山示范区':
        return [name, '昭山示范区', '昭山']
    if name == '湘潭九华示范区':
        return [name, '九华示范区', '九华']

    if name == '邯郸冀南新区':
        return [name, '冀南']
    if name == '五台山风景名胜区':
        return [name, '五台山']
    
    ss = ['经济技术开发区','经济开发区']
    for s in ss:
        if name.endswith(s):
            return [name, s, '开发区']
    
    if name.endswith('自治县'):
        x = name[:-3]
        for i in nations:
            x = x.replace(i,"")
        if len(x) == 0: return [name]
        ret = [name,x+"自治县",x+"县",x]
        return ret    
    for suffix in county_suffix:
        if name.endswith(suffix):
            x = name[:-len(suffix)]
            if len(x) <= 1: continue
            return [name, x]
    if name.endswith('自治旗'):
        x = name[:-len('自治旗')]
        return [name, x+'旗', x]
    elif name.endswith('旗'):
        return [name, name.rstrip('旗')]
    elif name == '保定白沟新城':
        return [name, '白沟']
    elif name.endswith('群岛'):
        return [name, name.rstrip('群岛')]
    elif name == '中沙群岛的岛礁及其海域':
        return [name, '中沙群岛', '中沙']
    return [name]

town_suffix = ['镇', '乡', '街道',]
def town_names(name):
    for suffix in town_suffix:
        if name.endswith(suffix):
            x = name[:-len(suffix)]
            if len(x) > 1:
                return [name, x]
            return [name,]
    if name.endswith('地区办事处'):
        x = name[:-len('地区办事处')]
        if len(x) > 1:
            return [name, x+"地区", x]
        else:
            return [name, x+"地区"]
    if name.endswith('街道办事处'):
        x = name[:-len('街道办事处')]
        if len(x) > 1:
            return [name, x+"街道", x]
        else:
            return [name, x+"街道"]
    return [name]

def village_names(name):
    ss = ["村委会","村民委员会","社区村委会","嘎查","嘎查村","嘎查村委员会"]
    for s in ss:
        if name.endswith(s):
            x = name[:-len(s)]
            if len(x) < 2: return [name]
            if x.endswith('村'):
                if len(x)>2: return [name, x, x[:-1]]
                return [name, x]
            else:
                return [name, x+'村', x]
    ss = ["生活区","工作区","工业园","工业区","虚拟社区"]
    for s in ss:
        if name.endswith(s):
            x = name[:-len(s)]
            if len(x) > 1:
                return [name, x]
            return [name]
        
    ss = ["社区居委会","社区居民委员会","居民委员会","居委会","社区","社区委员会","社区居委","社区居民委会"]
    for s in ss:
        if name.endswith(s):
            x = name[:-len(s)]
            if len(x) > 1:
                return [name, x+'社区', x+"小区", x]
            return [name, x+'社区', x+"小区"]

    return [name]

def names(f, name):
    return globals().get('%s_names' % f)(name)

lenmap = {2:"province",4:"city",6:"county",9:"town",12:"village"}

if __name__ == "__main__":
    import gzip
    import sys
    if len(sys.argv) < 2:
        print("Usage: python %s <infile>" % sys.argv[0])
        sys.exit(1)
    if sys.argv[1].endswith(".gz"): fp = gzip.open(sys.argv[1], 'rt')
    else: fp = open(sys.argv[1], 'rt')
    for line in fp:
        item = line.strip().split("\t")
        print("%s\t%s"%(item[0],','.join(names(lenmap[len(item[0])], item[1]))))

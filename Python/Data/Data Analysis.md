# Data Analysis

## Pandas

### 创建测试对象
```python
pd.DataFrame(np.random.rand(20,5))：创建20行5列的随机数组成的DataFrame对象
pd.Series(my_list)：从可迭代对象my_list创建一个Series对象
df.index = pd.date_range('1900/1/30', periods=df.shape[0])：增加一个日期索引
```

### Serise
Series 是一个带有 名称 和索引的一维数组，既然是数组，肯定要说到的就是数组中的元素类型，在 Series 中包含的数据类型可以是整数、浮点、字符串、Python对象等。Series 是一个带有 名称 和索引的一维数组，既然是数组，肯定要说到的就是数组中的元素类型，在 Series 中包含的数据类型可以是整数、浮点、字符串、Python对象等。
```python
# 构建索引
name = pd.Index(["Tom", "Bob", "Mary", "James"], name="name")
# 构建 Series
user_age = pd.Series(data=[18, 30, 25, 40], index=name, name="user_age_info")
user_age
```
手动指定数据类型
```python
# 指定类型为浮点型
user_age = pd.Series(data=[18, 30, 25, 40], index=name, name="user_age_info", dtype=float)
user_age
```
### DataFrame
DataFrame 是一个带有索引的二维数据结构，每列可以有自己的名字，并且可以有不同的数据类型。你可以把它想象成一个 excel 表格或者数据库中的一张表，DataFrame 是最常用的 Pandas 对象。

```python
orderdict = OrderedDict(mining.cleaned_nodes)
#nodes_dataframe =pd.DataFrame(orderdict)
nodes_dataframe.columns #行名称
nodes_dataframe.index.array #列名称
```

#### 数据选取
```python
df[col]：根据列名，并以Series的形式返回列
df[[col1, col2]]：以DataFrame形式返回多列
s.iloc[0]：按位置选取数据
s.loc['index_one']：按索引选取数据
df.iloc[0,:]：返回第一行
df.iloc[0,0]：返回第一列的第一个元素
```

#### 通过标签获取：
```python
df['A']
df[['A', 'B']]
df['A'][0]
df[0:10][['A', 'C']]
df.loc[:,['A','B']]  #行是所有的行，列取是A和B的
df.loc[:,'A':'C']
df.loc[0,'A']
df.loc[0:10,['A','C']]
```
#### 通过位置获取
```python
df.iloc[3]
df.iloc[3,3]
df.iloc[0:3,4:6]
df.iloc[1:5,:]
df.iloc[[1,2,4],[0,3]]
```

#### 通过布尔值过滤：
```
　　df[df['A']>0]
	　　df[df['A'].isin([1,3,5])]
	　　df[df<0] = 0
```

#### 查看、检查数据
```python
df.head(n)：查看DataFrame对象的前n行
df.tail(n)：查看DataFrame对象的最后n行
df.shape()：查看行数和列数
http://df.info()：查看索引、数据类型和内存信息
df.describe()：查看数值型列的汇总统计
s.value_counts(dropna=False)：查看Series对象的唯一值和计数
df.apply(pd.Series.value_counts)：查看DataFrame对象中每一列的唯一值和计数
```
#### 数据清理
```python
df.columns = ['a','b','c']：重命名列名
pd.isnull()：检查DataFrame对象中的空值，并返回一个Boolean数组
pd.notnull()：检查DataFrame对象中的非空值，并返回一个Boolean数组
df.dropna()：删除所有包含空值的行
df.dropna(axis=1)：删除所有包含空值的列
df.dropna(axis=1,thresh=n)：删除所有小于n个非空值的行
df.fillna(x)：用x替换DataFrame对象中所有的空值
s.astype(float)：将Series中的数据类型更改为float类型
s.replace(1,'one')：用‘one’代替所有等于1的值
s.replace([1,3],['one','three'])：用'one'代替1，用'three'代替3
df.rename(columns=lambda x: x + 1)：批量更改列名
df.rename(columns={'old_name': 'new_ name'})：选择性更改列名
df.set_index('column_one')：更改索引列
df.rename(index=lambda x: x + 1)：批量重命名索引
```


#### 数据处理：Filter、Sort和GroupBy
```python
df[df[col] > 0.5]：选择col列的值大于0.5的行
df.sort_values(col1)：按照列col1排序数据，默认升序排列
df.sort_values(col2, ascending=False)：按照列col1降序排列数据
df.sort_values([col1,col2], ascending=[True,False])：先按列col1升序排列，后按col2降序排列数据
df.groupby(col)：返回一个按列col进行分组的Groupby对象
df.groupby([col1,col2])：返回一个按多列进行分组的Groupby对象
df.groupby(col1)[col2]：返回按列col1进行分组后，列col2的均值
df.pivot_table(index=col1, values=[col2,col3], aggfunc=max)：创建一个按列col1进行分组，并计算col2和col3的最大值的数据透视表
df.groupby(col1).agg(np.mean)：返回按列col1分组的所有列的均值
data.apply(np.mean)：对DataFrame中的每一列应用函数np.mean
data.apply(np.max,axis=1)：对DataFrame中的每一行应用函数np.max, axis=0指的是逐行，axis=1指的是逐列。

- mean        #求平均值
- sum         #求和
- sort_index  #按行或列索引排序
- sort_values  #按值排序
- apply(func,axis=0)  #axis=0指的是逐行，axis=1指的是逐列。
        df.apply(lamada x:x.mean())  #按列求平均
        df.apply(lamada x:x['high']+x["low"])/2,axis=1)  #按列求平均（最高价和最低价的平均）
        df.apply(lamada x:x['high']+x["low"])/2,axis=1)  #按列求平均（最高价和最低价的平均）
- applymap(func) #将函数应用在DataFrame各个元素上
- map(func) #将函数应用在Series各个元素上
```
#### 数据合并
```python
df1.append(df2)：将df2中的行添加到df1的尾部
df.concat([df1, df2],axis=1)：将df2中的列添加到df1的尾部
df1.join(df2,on=col1,how='inner')：对df1的列和df2的列执行SQL形式的join
```

#### 数据统计
```python
df.describe()：查看数据值列的汇总统计
df.mean()：返回所有列的均值
df.corr()：返回列与列之间的相关系数
df.count()：返回每一列中的非空值的个数
df.max()：返回每一列的最大值
df.min()：返回每一列的最小值
df.median()：返回每一列的中位数
df.std()：返回每一列的标准差
```


#### DataFrame单列/多列进行运算（map, apply, transform, agg）


- 单列运算
在Pandas中，DataFrame的一列就是一个Series, 可以通过map来对一列进行操作：
```
df['col2'] = df['col1'].map(lambda x: x**2)
```
其中lambda函数中的x代表当前元素。可以使用另外的函数来代替lambda函数，例如：
```
define square(x):
    return (x ** 2)
df['col2'] = df['col1'].map(square)  
```

- 多列运算
要对DataFrame的多个列同时进行运算，可以使用apply，例如col3 = col1 + 2 * col2:

```
df['col3'] = df.apply(lambda x: x['col1'] + 2 * x['col2'], axis=1)
```

其中x带表当前行，可以通过下标进行索引。

- 分组运算
可以结合groupby与transform来方便地实现类似SQL中的聚合运算的操作：
```
df['col3'] = df.groupby('col1')['col2'].transform(lambda x: (x.sum() - x) / x.count())
```
在transform函数中x.sum()与x.count()与SQL类似，计算的是当前group中的和与数量，还可以将transform的结果作为一个一个映射来使用， 例如：
```
sumcount = df.groupby('col1')['col2'].transform(lambda x: x.sum() + x.count())
df['col1'].map(sumcount)
```

对col1进行一个map，得到对应的col2的运算值。


- 聚合函数
结合groupby与agg实现SQL中的分组聚合运算操作，需要使用相应的聚合函数：

```
df['col2'] = df.groupby('col1').agg({'col1':{'col1_mean': mean, 'col1_sum‘’: sum}, 'col2': {'col2_count': count}})
```
上述代码生成了col1_mean, col1_sum与col2_count列

---


### Data Visualization
#### Pandas Plotting

* Plotting methods allow for a handful of plot styles other than the default line plot. These methods can be provided as the kind keyword argument to plot(), and include:

    * `bar` or `barh` for bar plots
    * ‘hist’ for histogram
    * ‘box’ for boxplot
    * ‘kde’ or ‘density’ for density plots
    * area’ for area plots
    * scatter’ for scatter plots
    * hexbin’ for hexagonal bin plots
    * pie’ for pie plots

---
### Seaborn

> 我们将研究Seaborn，它是Python中另一个非常有用的数据可视化库。Seaborn库构建在Matplotlib之上，并提供许多高级数据可视化功能,尽管Seaborn库可以用于绘制各种图表，如矩阵图、网格图、回归图等，但在本文中，我们将了解如何使用Seaborn库绘制分布和分类图。在本系列的第二部分中，我们将了解如何绘制回归图、矩阵图和网格图.

- 分布图
 `sns.distplot(df['fs_roe'])`


- 联合分布图
 jointplot()用于显示各列的相互分布。您需要向jointplot传递三个参数。第一个参数是要在x轴上显示数据分布的列名。第二个参数是要在y轴上显示数据分布的列名。最后，第三个参数是数据帧的名称。
```python
#这里kind='reg'表示在画完连接图后，做出两者之间的线性关系
sns.jointplot(x='fs_roe', y='fs_roa_ttm', data=df,kind='reg')
```
kind =  {scatter,reg,resid,kde,hex}

- ***reg*** vs ***kde***

要将分类列的信息添加到pair plot中，可以将分类列的名称传递给hue参数。
```
sns.pairplot(dataset, hue='你想用来分类的列')
```

- Rug Plot
    ugplot()用于为数据集中的每个点沿x轴绘制小条。要绘制rug图，需要传递列的名称。我们来画个小的rug plot

- Bar Plot
barplot()用于显示分类列中的每个值相对于数字列的平均值。第一个参数是分类列，第二个参数是数值列，第三个参数是数据集。例如，如果您想知道各个股票营业收入这段时间的平均值，您可以使用如下的条形图。
`sns.barplot(x='timestamp', y='primary_per', data=eui_count_sorted)`


- 统计图
统计图与条形图类似，但是它显示特定列中类别的计数
`sns.countplot(x='primary_per', data=eui_count)`

***reg*** vs ***kde***
![reg](_v_images/20190429150302055_1634970608.png =710x)

Pair Plot paitplot()是一种分布图，它基本上为数据集中所有可能的数字列和布尔列的组合绘制联合图。您只需要将数据集的名称作为参数传递给pairplot()函数,从pair plot的输出中，可以看到一致预期中所有数字列和布尔列的分布图

要将分类列的信息添加到pair plot中，可以将分类列的名称传递给hue参数。

sns.pairplot(dataset, hue='你想用来分类的列')
![](_v_images/20190429150327147_1897745291.png =837x)

Bar Plot barplot()用于显示分类列中的每个值相对于数字列的平均值。第一个参数是分类列，第二个参数是数值列，第三个参数是数据集。例如，如果您想知道各个股票营业收入这段时间的平均值，您可以使用如下的条形图。 sns.barplot(x='timestamp', y='primary_per', data=eui_count_sorted)

统计图 统计图与条形图类似，但是它显示特定列中类别的计数 sns.countplot(x='primary_per', data=eui_count)


==asd==

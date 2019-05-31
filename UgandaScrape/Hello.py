# Some basic functions in Python
from __future__ import print_function

import matplotlib.pyplot
import numpy as np

import pandas as pd
import matplotlib.pyplot as plt
import pandas.plotting
import seaborn as sns

arr = np.arange(10, dtype=float).reshape(2, 5)
arr_col = arr[np.newaxis, :]
print(arr_col)
print(arr)
print(arr.shape)
# print(arr.reshape(5, 2))
print(arr_col.T)

columns = ['name', 'age', 'gender', 'job']
user1 = pd.DataFrame([['alice', 19, 'F', 'student'],
                      ['john', 26, 'M', 'student']], columns=columns)
user2 = pd.DataFrame([['eric', 22, 'M', 'student'],
                      ['paul', 58, 'F', 'manager']], columns=columns)
user3 = pd.DataFrame(dict(name=['peter', 'julie'], age=[33, 44],
                          gender=['M', 'F'],
                          job=['engineer', 'scientist']))
# print(user3)
user1.append(user2)
users = pd.concat([user1, user2, user3])
print(users)

user4 = pd.DataFrame(dict(name=['alice', 'john', 'eric', 'julie'],
                          height=[165, 180, 175, 171]))

# print(user4)
merge_inter = pd.merge(users, user4, on='name')
print("merge_inter\n", merge_inter)

users = pd.merge(users, user4, on='name', how='outer')
print('merge_inter_outer\n', users)

stacked = pd.melt(users, id_vars='name', var_name='variable', value_name='value')
print(stacked)

print(stacked.pivot(index='name', columns='variable', values='value'))

print('-------------\n', users)
type(users)
print('2.', users.head())
print('3.', users.tail())
print('4.', users.index)
print('5.', users.columns)
print('6.', users.dtypes)
print('7.', users.shape)
print('8.', users.values)
print('9.', users.info)

df = users.copy()
df.age.sort_values()
df.sort_values(by='age')
df.sort_values(by='age', ascending=False)
df.sort_values(by=['job', 'age'])
df.sort_values(by=['job', 'age'], inplace=True)
print("hello\n", df)

print(df.describe())
print(df.describe(include='all'))
print(df.describe(include=['object']))
print(df.groupby('job').mean())
print(df.groupby('job')['age'].mean())
print(df.groupby('job').describe(include='all'))

for grp, data in df.groupby('job'):
    print(grp, data)
print('\n')

print(df)
df = users.append(df.iloc[0], ignore_index=True)
print(df)
print(df.duplicated())

dff = users.copy()
df.describe(include='all')
df.height.isnull()
df.height.notnull()
print(df[df.height.notnull()])
print(df.height.isnull().sum)
df.height.isnull().sum()

print(df.isnull())
print(df.isnull().sum())

# df.dropna()
# print('meow\n', df)
# df.dropna(how='all')
# print('meow\n', df)

df = users.copy
# df.ix[df.height.isnull(), "height"]
# print(df['height'].mean())

size = pd.Series(np.random.normal(loc=175, size=20, scale=10))
size[:3] += 500
size_outlier_mean = size.copy()
size_outlier_mean[((size - size.mean()).abs() > 3 * size.std())] = size.mean
print(size_outlier_mean.mean())

MAD = 1.4826 * np.median(np.abs(size - size.median()))
size_outlier_mad = size.copy()
size_outlier_mad[((size - size.median()).abs() > 3 * MAD)] = size.median()
print(size_outlier_mad.mean(), size_outlier_mad.median())

x = np.linspace(0, 10, 50)
sinus = np.sin(x)
plt.plot(x, sinus)
plt.show()

# plt.plot(x, sinus, 'o')
# plt.show()
#
# cosinus = np.cos(x)
# plt.plot(x, sinus, '-b', x, sinus, 'ob', x, cosinus, '-r', x, cosinus, 'or')
# plt.xlabel("MEOW X")
# plt.ylabel("MEOW Y")
# plt.title('My first plot')
# plt.show()

# Plot the salary data
try:
    salary = pd.read_csv("../datasets/salary_table.csv")
except:
    url = 'https://raw.github.com/neurospin/pystatsml/master/datasets/salary_table.csv'
    salary = pd.read_csv(url)
df = salary

plt.figure(figsize=(6, 5))
symbols_manage = dict(Y='*', N='.')
colors_edu = {'Bachelor': 'r', 'Master': 'g', 'Ph.D': 'blue'}

print(salary, '\n-----------------\n')


for values, data_Chi in salary.groupby(['education', 'management']):
    edu, manager = values
    plt.scatter(data_Chi['experience'], data_Chi['salary'], marker=symbols_manage[manager], color=colors_edu[edu],
                s=150, label=manager+"/"+edu)
plt.xlabel('Experience')
plt.ylabel('Salary')
# Loc=1: up-right, Loc=2: up-left, Loc=3: bottom-left, Loc=4: bottom-right,... explore later
plt.legend(loc=4)
plt.show()
plt.savefig("chi.pdf")
plt.close()
print(salary)

sns.boxplot(x="education", y="salary", hue="management", data=salary)
# Have to use plt.show after plotting the graphs, if not, plots will not be shown
plt.show()
sns.boxplot(x="management", y="salary", hue="education", data=salary)
sns.stripplot(x="management", y="salary", hue="education", data=salary,
              jitter=True, dodge=True, linewidth=1)
plt.show()

f, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
i = 0
for edu, d in salary.groupby(['education']):
    print(edu, d)
    sns.distplot(d.salary[d.management == 'Y'], color='b', bins=10, label='Manager',
                 ax=axes[i])
    sns.distplot(d.salary[d.management == 'N'], color='r', bins=10, label='Employee',
                 ax=axes[i])
    axes[i].set_title(edu)
    axes[i].set_ylabel('Density')
    i += 1
    ax = plt.legend()
plt.show()
ax = sns.barplot(x="management", y="salary", hue="education", data=salary)
plt.show()
ax = sns.boxenplot(x="management", y="salary", hue="education", data=salary)
plt.show()
ax = sns.catplot(x="management", y="salary", hue="education", data=salary)
plt.show()
ax = sns.dogplot()
plt.show()
ax = sns.violinplot(x='salary', data=salary, bw=.15)
plt.show()
ax = sns.violinplot(x='management', y='salary', hue='education', data=salary)
plt.show()

# show the horizontal grid for the plots
sns.set(style='whitegrid')
tips = sns.load_dataset('tips')
print(tips.head())
ax = sns.violinplot(x=tips['total_bill'])
plt.show()
ax = sns.violinplot(x='day', y='total_bill', data=tips, palette='muted')
plt.show()
ax = sns.violinplot(x='day', y='total_bill', hue='time', data=tips, palette='muted', split=True)
plt.show()
g = sns.PairGrid(salary, hue='management')
g.map_diag(plt.hist)
g.map_offdiag(plt.scatter)
ax = g.add_legend()
plt.show()
sns.set(style='whitegrid')
sns.set(style='darkgrid')
fmri=sns.load_dataset('fmri')
ax=sns.pointplot(x='timepoint', y='signal', hue='region', style='event', data=fmri)
plt.show()

# Load dataset
filename = 'D:/Kitty/NUS/3-IT_Professionalism/meow/iris.data'
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(filename, names=names)

# shape
print(dataset.shape)

# head: First 20 rows of the dataset
print(dataset.head(20))

# descriptions
print(dataset.describe())

# class distribution
print(dataset.groupby('class').size())

# box and whisker plots
dataset.plot(kind='box', subplots=True, layout=(2, 2), sharex=False, sharey=False)
matplotlib.pyplot.show()

# histograms
dataset.hist()
matplotlib.pyplot.show()

# scatter plot matrix
pandas.plotting.scatter_matrix(dataset)
matplotlib.pyplot.show()



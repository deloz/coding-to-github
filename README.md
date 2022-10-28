# 批量迁移Coding仓库到Github

使用了 [Coding openapi接口](https://coding.net/help/openapi) 和 [Github token](https://github.com/settings/tokens)

### 1, 申请 Coding 的个人访问令牌token

![coding-token](https://user-images.githubusercontent.com/685167/198686187-b544c048-132e-41a6-aaf2-b19ce2dab75a.png)

### 2, 申请 Github 的token

 ![Github token](https://user-images.githubusercontent.com/685167/198687197-af9d6372-aed4-499d-993e-b4550c2593da.png)


### 3, 修改 `main.py` 中 `GITHUB_TOKEN`和`CODING_TOKEN`的值 
 
### 4，执行脚本
```
# 安装依赖
pip3 install -r requirements.txt  
# 开始迁移
python3 main.py
```

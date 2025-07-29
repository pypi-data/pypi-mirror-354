# tea

## 介绍

tea：TEA算法由剑桥大学计算机实验室的David Wheeler和Roger Needham于1994年发明。它是一种分组密码算法，其明文密文块为64比特，密钥长度为128比特。TEA算法利用不断增加的Delta(黄金分割率)值作为变化，使得每轮的加密是不同，该加密算法的迭代次数可以改变，**本算法的迭代次数为32轮**。

本软件包已上传到 pypi, 可通过 pip 进行安装：

```
pip install tea-python
```

## 示例代码：

```python
import tea

if __name__ == '__main__':
    key = "1122334455667788".encode()
    origin = bytearray()

    for i in range(16):
        origin.append(i)

    print('原数据:  ', origin.hex())
    encrypt_data = tea.encrypt(origin, key)
    print('加密数据:', encrypt_data.hex())
    decrypt_data = tea.decrypt(encrypt_data, key)
    print('解密数据:', decrypt_data.hex())

```

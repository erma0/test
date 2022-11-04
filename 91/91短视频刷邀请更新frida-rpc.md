目标APP：91短视频
> 之前发过一篇文章，app升级算法之后还没来得及更新，文章就被举报404了，悲哀，今天厚码写一下新版过程，就不贴源码了，放github需要自取，我看老六还怎么举报。

## 工具准备

- [HTTP Debugger Professional v9.11](https://down.52pojie.cn/Tools/Network_Analyzer/HTTP_Debugger_Professional_v9.11.zip)
- [雷电模拟器9绿色去广告版](https://www.52pojie.cn/forum.php?mod=viewthread&tid=1692394)
- 算法助手（通用hook插件）

> **用到的工具**及**配置好的雷电模拟器系统备份**在[release页面](https://github.com/erma0/test/releases/tag/ld)下载

> PS. 直接使用备份的系统，环境都配置好了，打开frida转发端口就能用。

> 自行配置步骤：模拟器设置system可写并开启root，用MagiskDelta刷面具，删除自带的su文件，刷入LSPosed，安装算法助手插件，用FridaHooker安装Frida。算法助手中打开总开关和算法分析的3个开关，开启Frida，通过adb转发端口，打开HTTP Debugger Pro抓包（需安装证书到系统分区）

## 分析过程
工具都配置好后，打开目标APP，直到成功绑定邀请码。
（我测试过程中装完证书直接就可以正常抓包，说抓不到的可以试试在算法助手里打开JustTrustMe）

返回算法助手查看，发现没有aes加密，竟然和以前加密方式不同了

不过回算法助手可以看到sign还是有的，依然是老方法，sha256+md5

apk拖到GDA中，定位到算法助手中sign的调用堆栈位置，很容易发现加密点

按x查看交叉引用，最终定位到了sojm.so

```
package com.qq.lib.EncryptUtil;
import java.lang.System;
import java.lang.String;
import java.lang.Object;

public class EncryptUtil	// class@000900
{
    static {
       System.loadLibrary("sojm");
    }
    public void EncryptUtil(){
       super();
    }
    public static native String decrypt(String p0,String p1);
    public static native String decryptHls(String p0,String p1);
    public static native byte[] decryptImg(byte[] p0,int p1,String p2);
    public static native byte[] decryptImg2(byte[] p0,int p1,String p2);
    public static native String encrypt(String p0,String p1);
}
```

由于不会分析so，尝试一番后无果，且模拟器frida无法hook到第三方APP的so，手上又没有真机，遂放弃

改用frida-rpc，供python程序直接调用加密方法，除了使用过程比较麻烦，貌似也没什么大问题

学习了一番frida，直接开始改代码，还是之前的源码，只是改一改加密解密方法

最终hook到com.qq.lib.EncryptUtil这里就行，不用到so里面，反正只是外部调用而已

## Python源码
[https://github.com/erma0/test/blob/main/91/frida91.py](https://github.com/erma0/test/blob/main/91/frida91.py)
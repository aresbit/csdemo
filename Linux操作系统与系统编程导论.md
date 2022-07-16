# Linux操作系统与系统编程导论

程序视角下的OS： 程序 + syscall 一条系统调用指令。

```c
#include <unistd.h>
long syscall(long number, ...);
```



以Linux x86_64系统调用为例。即处理器指令集默认为x86_64指令集

为了解系统编程，需了解Linux内核

如果想对Linux内核做进一步的**定制**，那么了解Linux的全部系统调用就是一个很好的帮助。

即需深入了解每个Linux x86_64系统调用的功能、用法与实现细节。

- 环境配置：

  - Linux内核： V5.4
  - glibc-2.31

  - 位置：Linux内核源码的`arch/x86/entry/syscalls/syscall_64.tbl`
  - RTFM： 功能、用法基于其相应的manual page，可在[man7.org](https://www.man7.org/linux/man-pages/)中查看。
  - OS： 在Ubuntu 20.04中进行验证代码。



## [系统调用对照表](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/#系统调用对照表)

每个系统调用名都超链接到了其在本仓库中对应的文章。

| 名称                                                         | 系统调用号 | 头文件          | 内核实现                       |
| ------------------------------------------------------------ | ---------- | --------------- | ------------------------------ |
| [`read`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/read-pread64-readv-preadv-preadv2.html) | 0          | `unistd.h`      | `fs/read_write.c`              |
| [`write`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/write-pwrite64-writev-pwritev-pwritev2.html) | 1          | `unistd.h`      | `fs/read_write.c`              |
| [`open`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/open-openat-name_to_handle_at-open_by_handle_at-open_tree.html) | 2          | `fcntl.h`       | `fs/open.c`                    |
| [`close`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/close.html) | 3          | `unistd.h`      | `fs/open.c`                    |
| [`stat`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/stat-fstat-lstat-newfstatat-statx.html) | 4          | `sys/stat.h`    | `fs/stat.c`                    |
| [`fstat`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/stat-fstat-lstat-newfstatat-statx.html) | 5          | `sys/stat.h`    | `fs/stat.c`                    |
| [`lstat`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/stat-fstat-lstat-newfstatat-statx.html) | 6          | `sys/stat.h`    | `fs/stat.c`                    |
| [`poll`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/poll-select-pselect6-ppoll.html) | 7          | `poll.h`        | `fs/select.c`                  |
| [`lseek`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/lseek.html) | 8          | `unistd.h`      | `fs/read_write.c`              |
| [`mmap`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/memory_management/mmap-munmap-mremap-msync-remap_file_pages.html) | 9          | `sys/mman.h`    | `arch/x86/kernel/sys_x86_64.c` |
| [`munmap`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/memory_management/mmap-munmap-mremap-msync-remap_file_pages.html) | 11         | `sys/mman.h`    | `mm/mmap.c`                    |
| [`pread64`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/read-pread64-readv-preadv-preadv2.html) | 17         | `unistd.h`      | `fs/read_write.c`              |
| [`pwrite64`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/write-pwrite64-writev-pwritev-pwritev2.html) | 18         | `unistd.h`      | `fs/read_write.c`              |
| [`readv`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/read-pread64-readv-preadv-preadv2.html) | 19         | `sys/uio.h`     | `fs/read_write.c`              |
| [`writev`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/write-pwrite64-writev-pwritev-pwritev2.html) | 20         | `sys/uio.h`     | `fs/read_write.c`              |
| [`select`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/poll-select-pselect6-ppoll.html) | 23         | `sys/select.h`  | `fs/select.c`                  |
| [`mremap`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/memory_management/mmap-munmap-mremap-msync-remap_file_pages.html) | 25         | `sys/mman.h`    | `mm/mremap.c`                  |
| [`msync`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/memory_management/mmap-munmap-mremap-msync-remap_file_pages.html) | 26         | `sys/mman.h`    | `mm/msync.c`                   |
| [`epoll_create`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/epoll_create-epoll_wait-epoll_ctl-epoll_pwait-epoll_create1.html) | 213        | `sys/epoll.h`   | `fs/eventpoll.c`               |
| [`remap_file_pages`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/memory_management/mmap-munmap-mremap-msync-remap_file_pages.html) | 216        | `sys/mman.h`    | `mm/mmap.c`                    |
| [`epoll_ctl`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/epoll_create-epoll_wait-epoll_ctl-epoll_pwait-epoll_create1.html) | 232        | `sys/epoll.h`   | `fs/eventpoll.c`               |
| [`epoll_wait`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/epoll_create-epoll_wait-epoll_ctl-epoll_pwait-epoll_create1.html) | 233        | `sys/epoll.h`   | `fs/eventpoll.c`               |
| [`openat`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/open-openat-name_to_handle_at-open_by_handle_at-open_tree.html) | 257        | `fcntl.h`       | `fs/open.c`                    |
| [`newfstatat`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/stat-fstat-lstat-newfstatat-statx.html) | 262        | `sys/stat.h`    | `fs/stat.c`                    |
| [`pselect6`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/poll-select-pselect6-ppoll.html) | 270        | `sys/select.h`  | `fs/select.c`                  |
| [`ppoll`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/poll-select-pselect6-ppoll.html) | 271        | `poll.h`        | `fs/select.c`                  |
| [`epoll_pwait`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/epoll_create-epoll_wait-epoll_ctl-epoll_pwait-epoll_create1.html) | 281        | `sys/epoll.h`   | `fs/eventpoll.c`               |
| [`eventfd`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/eventfd-eventfd2.html) | 284        | `sys/eventfd.h` | `fs/eventfd.c`                 |
| [`eventfd2`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/eventfd-eventfd2.html) | 290        | `sys/eventfd.h` | `fs/eventfd.c`                 |
| [`epoll_create1`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/epoll_create-epoll_wait-epoll_ctl-epoll_pwait-epoll_create1.html) | 291        | `sys/epoll.h`   | `fs/eventpoll.c`               |
| [`preadv`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/read-pread64-readv-preadv-preadv2.html) | 295        | `sys/uio.h`     | `fs/read_write.c`              |
| [`pwritev`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/write-pwrite64-writev-pwritev-pwritev2.html) | 296        | `sys/uio.h`     | `fs/read_write.c`              |
| [`name_to_handle_at`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/open-openat-name_to_handle_at-open_by_handle_at-open_tree.html) | 303        | `fcntl.h`       | `fs/fhandle.c`                 |
| [`open_by_handle_at`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/open-openat-name_to_handle_at-open_by_handle_at-open_tree.html) | 304        | `fcntl.h`       | `fs/fhandle.c`                 |
| [`preadv2`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/read-pread64-readv-preadv-preadv2.html) | 327        | `sys/uio.h`     | `fs/read_write.c`              |
| [`pwritev2`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/write-pwrite64-writev-pwritev-pwritev2.html) | 328        | `sys/uio.h`     | `fs/read_write.c`              |
| [`statx`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/stat-fstat-lstat-newfstatat-statx.html) | 332        | `linux/stat.h`  | `fs/stat.c`                    |
| [`open_tree`](https://evian-zhang.github.io/introduction-to-linux-x86_64-syscall/src/filesystem/open-openat-name_to_handle_at-open_by_handle_at-open_tree.html) | 428        | 无              | `fs/namespace.c`               |



## 系统调用

创建子进程的操作，Linux内核提供了`fork`这个系统调用作为接口。那么，如果用户态程序想调用这个内核提供的接口，其对应的汇编语句为

```assembly
movq $57, %rax
syscall
```

`fork`这个系统调用的系统调用号是57,

`syscall`这个指令会先查看此时RAX的值，然后找到系统调用号为那个值的系统调用

这就是让内核执行了`fork`。

## 调用约定

系统调用往往会有许多参数，比如说`open`这个打开文件的系统操作，我们可以在`include/linux/syscalls.h`中找到其对应的C语言接口为

```c
asmlinkage long sys_open(const char __user *filename, int flags, umode_t mode);

```

如果要调用`open`系统调用，那么步骤是：

1. 将`pathname`放入`rdi`寄存器
2. 将`flags`放入`rsi`寄存器
3. 将`mode`放入`rdx`寄存器
4. 将`open`的系统调用号2放入`rax`寄存器
5. 执行`syscall`指令
6. 返回值位于`rax`寄存器

可用逆向工具查看汇编代码，通过类似以上六步的方法，确定一个系统调用的相关信息

该规范就称为内核接口的调用约定

其中gcc提供了一个标签`asmlinkage`来标记这个函数是内核接口的调用约定，

以区别用户态函数传参。

我们平时写的代码中，99%不会直接用到上述的系统调用方法。当我们真的去写一个C程序时：会有glibc提供用户态必需系统调用接口函数及必需函数（比如malloc）。

我们在Linux上编写的程序，通常都会链接到glibc的动态链接库。可用ldd查看其链接的动态链接库。

## glibc 封装

glibc是Linux系统中最底层的API，几乎其它任何的运行库都要依赖glibc。

glibc最主要的功能就是对系统调用的封装

fopen函数打开文件：要触发系统中的sys_open系统调用。

除了封装系统调用，glibc自身也提供了一些上层应用函数必要的功能,如string,malloc,stdlib等。

## RTFM

- glibc https://www.gnu.org/software/libc/manual/

- System Call Wrappers https://sourceware.org/glibc/wiki/SyscallWrappers
- https://www.man7.org/linux/man-pages/

内核接口

以open为例，

在Linux内核中，可以在`include/linux/syscalls.h`文件中找到系统调用函数的声明（会加上`sys_`前缀）。

其实现则是使用`SYSCALL_DEFINEn`这个宏。

在`fs/open.c`中可以看到：

```c
SYSCALL_DEFINE3(open, const char __user *, filename, int, flags, umode_t, mode)
{
    /* ... */
}
```

- 内核提供了一个接口，接受三个参数
- 这个接口叫`open`
- 第一个参数的类型是`const char __user *`，参数名为`filename`
- 第二个参数的类型是`int`，参数名是`flags`
- 第三个参数的类型是`umode_t`，参数名是`mode`

系统调用按对象可分为文件系统，内存管理，进程管理，网络等各部分，对应OS课程各部。


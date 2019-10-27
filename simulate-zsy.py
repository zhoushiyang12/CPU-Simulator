
#一些辅助的函数
def bit_print(num):           #输出为2进制
    if (num & 0x80)== 0x80:
        n7 = 1
        print(1,end='')
    else:
        n7 = 0
        print(0,end='')

    if (num & 0x40)== 0x40:
        n6 = 1
        print(1,end='')
    else:
        n6 = 0
        print(0,end='')
    if (num & 0x20)== 0x20:
        n5 = 1
        print(1,end='')
    else:
        n5 = 0
        print(0,end='')

    if (num & 0x10)== 0x10:
        n4 = 1
        print(1,end='')
    else:
        n4 = 0
        print(0,end='')

    if (num & 0x08)== 0x08:
        n3 = 1
        print(1,end='')
    else:
        n3 = 0
        print(0,end='')

    if (num & 0x04)== 0x04:
        n2 = 1
        print(1,end='')
    else:
        n2 = 0
        print(0,end='')

    if (num & 0x02)== 0x02:
        n1 = 1
        print(1,end='')
    else:
        n1 = 0
        print(0,end='')

    if (num & 0x01)== 0x01:
        n0 = 1
        print(1,end='')
    else:
        n0 = 0
        print(0,end='')


def conv_num(num):     #32bit转换为十进制
    return  num[0]+num[1]*256+num[2]*256*256+num[3]*256*256*256

def num_add_4byte(n=None,byte4=None):
    bytes4 = bytearray(4)
    num = 0
    num =n
    for i in range(4):bytes4[i]=byte4[i]     #python的机制是传对象，不是c++传参，切记，所以此处实例化一个新的

    if num + bytes4[0] < 256:
        bytes4[0] += num
    elif (num + bytes4[0]) // 256 + bytes4[1] < 256:
        bytes4[1] = (num + bytes4[0]) // 256 + bytes4[1]
        bytes4[0] = (num + bytes4[0]) % 256
    elif ((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2] < 256:
        bytes4[2] = ((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2]
        bytes4[1] = ((num + bytes4[0]) // 256 + bytes4[1]) % 256
        bytes4[0] = (num + bytes4[0]) % 256
    elif (((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2]) // 256 + bytes4[3] < 256:
        bytes4[3] = (((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2]) // 256 + bytes4[3]
        bytes4[2] = (((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2]) % 256
        bytes4[1] = ((num + bytes4[0]) // 256 + bytes4[1]) % 256
        bytes4[0] = (num + bytes4[0]) % 256
    else:
        bytes4[3] = ((((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2]) // 256 + bytes4[3]) % 256
        bytes4[2] = (((num + bytes4[0]) // 256 + bytes4[1]) // 256 + bytes4[2]) % 256
        bytes4[1] = ((num + bytes4[0]) // 256 + bytes4[1]) % 256
        bytes4[0] = (num + bytes4[0]) % 256
        print("！！！！！！num+bytes4益处啦！！！！！！！")
    return bytes4


'''
32位处理器有16个寄存器，每个寄存器有各自的名字。
16个寄存器：EAX、EBX、ECX、EDX、ESI、EDI、ESP、EBP、ES、CS、SS、DS、FS、GS、EIP、EFLAGS。
64位处理器有16个寄存器，每个寄存器有各自的名字。
16个寄存器：RAX、RBX、RCX、RDX、RSI、RDI、RBP、RSP、CS、DS、ES、SS、FS、GS、RIP、RFLAGS。
'''
class Register:
    def __init__(self):
        self.cs= bytearray(4)                                                                  #程序基址寄存器寄存器32-bit，高位在右。
        self.cs[0]=0b11111111                                                                  #默认程序段基址为  （255）H
        self.ds = bytearray(4)                                                                #数据基址寄存器32-bit，高位在右。      默认数据段基址为  （0）H
        self.com_reg = [bytearray(4) for row in range(30)]                                    # 30个32-bit的通用寄存器，高位在右。
    def Write_R(self,WriteRegister,WriteData):         #寄存器写操作4个字节，高位在右。
        try:
            for i in range(4):                       #每个Register是4个字节
                self.com_reg[WriteRegister][i]=WriteData[i]
            print('将数据',end='')
            for i in range(4):
                bit_print(WriteData[i])        #以二进制输出
            print('写入寄存器%d\n'%WriteRegister,end='')
        except:
            print('Register Write error！')
    def Read_R(self,ReadRegister):   #模拟读操作，ReadRegister是一个列表，包含所读入的两个寄存器的地址，
        try:
            Readdata=bytearray()
            for j in range(4):
                Readdata.append(self.com_reg[ReadRegister][j])

            print('将数据',end='')
            for j in range(4):
                bit_print(Readdata[j])
            print('从寄存器%d读出\n'%ReadRegister,end='')
            return Readdata
        except:
            print('Register Read error！')


class ALU:
    def Add1(self,x1,x2):                                                #加法
        result=[0 for i in range(4)]
        acc=0b0                                                        #溢出
        for i in range(4):                                             #高位在右，按照从低到高的顺序加
            tmp = x1[i] + x2[i] + acc
            acc = 0b0                                                  #溢出清零
            if (tmp > 0B11111111):
                tmp = 0B00000000
                acc = 0b1
            result[i]=tmp

        print('将',end='')
        for i in range(4):
            print(x1[i],end='')
        print('和',end='')
        for i in range(4):
            print(x2[i],end='')
        print('相加，得到',end='')
        for i in range(4):
            print(result[i],end='')
        if acc == 0b1:
            print('\n','！！！！！！！加法器溢出！！！！！！！！','\n',end='')
            print("ACC_flag=1")
        return result

class Memory:
    def __init__(self):
        self.data_mem = bytearray(4096)          #4096个8-bit内存，高位在右
    def Write_M(self,Address,WriteData):         #写内存，应为寄存器为32bits，4字节。数据总线宽度为32bits所以数据每次以4字节读入或读出
        try:
            newaddress = conv_num(Address)
            lenth=len(WriteData)
            for i in range(lenth):
                self.data_mem[newaddress+i]=WriteData[i]
            print('将数据',end='')
            for i in range(lenth):
                bit_print(WriteData[i])

            print('写入内存地址%d--%d:\n'%(newaddress,newaddress+lenth),end='\n')
        except:
            print('Memory Write Error!')
    def Read_M(self,Address,num=4):                                         #从内存读数，默认一次读4byte（32bits），num为字节数
        try:
            Readdata = []                                               #因为寄存器32位，所以一次读出4字节32bit
            newaddress = conv_num(Address)
            # print("newaddress：",newaddress)
            for i in range(num):
                Readdata.append(self.data_mem[newaddress+i])           #因为寄存器32位，所以一次读出4字节32bit
                # print('将数据',end='')
            # for j in range(num):
                # bit_print(Readdata[j])
            # print('从内存%d--%d读出:\n'%(newaddress,newaddress+num),end='\n')
            return Readdata
        except:
            print('Memory Read Error!')

class Controller(Register, Memory, ALU):
    def __init__(self):
        super(Register, self).__init__()
        super(Memory, self).__init__()
        super(Controller, self).__init__()

        self.pc = 0  # 程序计数器
        self.sp = 0  # 程序计数器
        self.psw = 1  # 程序状态字,这里只定义了一个状态程序运行和结束
        self.ins_reg = []  # 指令寄存器

    def Load(self,RegAddress,MemAddress):
        # print("load add:",MemAddress)
        tmp = Memory.Read_M(self,Address=MemAddress,num = 4)
        # print(tmp)
        Register.Write_R(self,RegAddress, tmp)

    def Store(self,RegAddress, MemAddress):
        tmp = Register.Read_R(self,RegAddress)
        Memory.Write_M(self,MemAddress, tmp)

    def Add(self,RegAddress3, RegAddress1, RegAddress2):
        tmp1 = Register.Read_R(self,RegAddress1)
        tmp2 = Register.Read_R(self,RegAddress2)
        tmp3 = ALU.Add1(self,tmp1, tmp2)
        Register.Write_R(self,RegAddress3, tmp3)

    def deconde(self):
        instruction = bytearray()
        cs = self.cs
        p  = self.sp
        tem = bytearray(1)
        while True:
            cs = num_add_4byte(self.sp, self.cs)                     #计算偏移后的地址,注意python传的是对象
            # print("cs:",cs)
            tem = self.Read_M(cs, num=1)
            if tem[0] == bytearray('\n', encoding='ascii')[0]:
                self.sp += 1
                break
            # print('read:', type(tem))
            instruction.append(tem[0])                                 #从数据段读出一条指令
            self.sp += 1
        # print(instruction)
        # print("读出一条指令：",instruction.decode(encoding='ascii'))
        ins = instruction.decode(encoding='utf-8').split(' ')
        if ins[0] == "Done":                                            # 模拟一下解码器，有点LOW
            self.psw = 0
            print("Program Over!")
        if ins[0] == "Load":                                           #模拟一下解码器，有点LOW
            print(ins)
            if ins[1] == "r1": ins[1] = 1
            if ins[1] == "r2": ins[1] = 2
            if ins[1] == "r3": ins[1] = 3

            address = num_add_4byte(int(ins[2])*4,self.ds)
            # print(ins[1],address)
            self.Load(ins[1],address)
        if ins[0] == "Store":  # 模拟一下解码器，有点LOW
            print(ins)
            if ins[1] == "r1": ins[1] = 1
            if ins[1] == "r2": ins[1] = 2
            if ins[1] == "r3": ins[1] = 3
            # address2 = bytearray(4)
            # for i in range(4):address2[i]=self.ds[i]
            # address2[1] += int(ins[2])*4

            address = num_add_4byte(int(ins[2]) * 4, self.ds)
            self.Store(ins[1],address)
        if ins[0] == "Add":  # 模拟一下解码器，有点LOW
            print(ins)
            if ins[1] == "r1": ins[1] = 1
            if ins[1] == "r2": ins[1] = 2
            if ins[1] == "r3": ins[1] = 3
            if ins[2] == "r1": ins[2] = 1
            if ins[2] == "r2": ins[2] = 2
            if ins[2] == "r3": ins[2] = 3
            if ins[3] == "r1": ins[3] = 1
            if ins[3] == "r2": ins[3] = 2
            if ins[3] == "r3": ins[3] = 3
            self.Add( ins[1], ins[2], ins[3])
        return instruction.decode(encoding='utf-8')

    def run(self):
        while self.psw:
            print("The %dth instruction!-------"%(self.pc+1),end="")
            self.deconde()
            self.pc += 1


if __name__ == '__main__':
    #程序初始化
    writedata1 = [0B00001111,0B00000000,0B00000000,0B00000001]   # 输入两个32bit（4byte）的数，每个byte为8位，0-255  小端存储
    writedata2 = [0B00001111,0B00000000,0B00000000,0B00000001]   # 输入两个32bit（4byte）的数，每个byte为8位，0-255

    program="Load r1 0\nLoad r2 1\nAdd r3 r1 r2\nStore r3 3\nDone\n".encode(encoding='utf-8')
    print(program.__len__())
    controller = Controller()
    controller.Write_M(controller.ds, writedata1+writedata2)
    controller.Write_M(controller.cs, program)

    #程序开始运行
    controller.run()









# 数控编程可视化 ver_0.28
# 待完成：顺圆弧优化，逆圆弧，增加缩放，语法高亮，美化UI...

import tkinter.ttk
import re
import math
import time

# 把X10 Y10转换成X:10.0 Y:10.0
def list2dict(sample):
    res = {}
    for i in range(0, len(sample), 2):
        try:
            v = float(sample[i+1])
            if int(v) == v:
                v = int(v)
        except:
            time.sleep(1)
            clear()
        else:
            res.update({sample[i]: v})
    return res

# 已知两点半径求圆心
def f_center(p1, p2, r, g):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    c1 = (x2**2 - x1**2 + y2**2 - y1**2) / (2*(x2 - x1))
    c2 = (y2 - y1) / (x2 - x1)
    a = 1 + c2**2
    b = 2*(x1 - c1)*c2 - 2*y1
    c = (x1 - c1)**2 + y1**2 - r**2
    if g == 2:
        y0 = (-b - math.sqrt(b**2 - 4*a*c)) / (2 * a)
        x0 = c1 - c2 * y0
        return (x0, y0)
    else:
        y0 = (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a)
        x0 = c1 - c2 * y0
        return (x0, y0)

# 绘制图形，预留Z方向（挖坑）
def draw_line(c_g, point, c_x, c_y, c_z, c_i, c_j, c_k, c_r):
    c_g = int(c_g)
    match c_g:
        case 0:
            # 快速进给
            canvas.create_line(250+point[0], 250-point[1], 250+c_x, 250-c_y, fill='red')
            pass
        case 1:
            # 工速进给
            canvas.create_line(250+point[0], 250-point[1], 250+c_x, 250-c_y, fill='green', width=2)
        case 2:
            # 顺圆
            o = f_center(point, (c_x, c_y), c_r, c_g)
            x2 = o[0] - c_r
            y2 = o[1] + c_r
            x4 = o[0] + c_r
            y4 = o[1] - c_r
            angle_e = math.atan((c_y - o[1]) / (c_x - o[0])) - math.atan((point[1] - o[1]) / (point[0] - o[0]))
            angle_s = math.atan((point[1] - o[1]) / (point[0] - o[0]))
            angle_e, angle_s = math.degrees(angle_e), math.degrees(angle_s)
            if c_x > o[0]:
                angle_e = 180 - angle_e
            canvas.create_arc(250+x2, 250-y2, 250+x4, 250-y4, extent=-angle_e, start=angle_s, outline='yellow', style = 'arc', width=2)
            canvas.create_line(250+point[0], 250-point[1], 250+c_x, 250-c_y, fill='grey', width=1)
        case 3:
            # 逆圆
            o = f_center(point, (c_x, c_y), c_r, c_g)
            x2 = o[0] - c_r
            y2 = o[1] + c_r
            x4 = o[0] + c_r
            y4 = o[1] - c_r
            angle_e = math.atan((c_y - o[1]) / (c_x - o[0])) - math.atan((point[1] - o[1]) / (point[0] - o[0]))
            angle_s = math.atan((point[1] - o[1]) / (point[0] - o[0]))
            angle_e, angle_s = math.degrees(angle_e), math.degrees(angle_s)
            if c_x < o[0]:
                angle_e = 180 - angle_e
            canvas.create_arc(250+x2, 250-y2, 250+x4, 250-y4, extent=-angle_e, start=angle_s, outline='yellow', style = 'arc', width=2)
            canvas.create_line(250+point[0], 250-point[1], 250+c_x, 250-c_y, fill='grey', width=1)
        


# 生成
def submit():
    code = code_text.get('1.0', 'end')
    code = code.strip()
    terminal.config(state='normal')
    c_x = c_y = c_g = c_i = c_j = c_k = c_r = c_z = 0
    zoom = 5
    # 缩放倍率，默认画布XY:[-250,250]
    for i in code.split('\n'):
        # c_xy为当前点的值
        # point为上一个点的值
        point = (c_x, c_y, c_z)
        if len(i):
            i = re.sub('[A-Z]',lambda x: ' '+x.group(0)+' ', i)
            i = i.split()
            temp = list2dict(i)
            for key in temp.keys():
                match key:
                    case 'N':
                        c_n = int(temp.get(key))
                        terminal.insert('end', '第{}行: '.format(c_n))
                    case 'M':
                        c_m = temp.get(key)
                        # terminal.insert('end', '{} '.format(c_m))
                    case 'X':
                        c_x = temp.get(key) * zoom
                        terminal.insert('end', 'X移动到{} '.format(c_x))
                    case 'Y':
                        c_y = temp.get(key) * zoom
                        terminal.insert('end', 'Y移动到{} '.format(c_y))
                    case 'Z':
                        c_z = temp.get(key) * zoom
                        terminal.insert('end', 'Z移动到{} '.format(c_z))
                    case 'I':
                        c_i = temp.get(key) * zoom
                    case 'J':
                        c_j = temp.get(key) * zoom
                    case 'K':
                        c_k = temp.get(key) * zoom
                    case 'R':
                        c_r = temp.get(key) * zoom
                    case 'U':
                        c_u = temp.get(key) * zoom
                    case 'P':
                        c_p = temp.get(key) * zoom
                    case 'Q':
                        c_q = temp.get(key) * zoom
                    case 'F':
                        c_f = temp.get(key)
                        terminal.insert('end', '进给量{} '.format(c_f))
                    case 'S':
                        c_s = temp.get(key)
                        terminal.insert('end', '主轴转速{} '.format(c_s))
                    case 'G':
                        c_g = temp.get(key)
                        match c_g:
                            case 0:
                                g_state = '快速进给 '
                            case 1:
                                g_state = '工速进给 '
                            case 2:
                                g_state = '顺圆进给 '
                            case 3 :
                                g_state = '逆圆进给 '
                        terminal.insert('end', g_state)
            draw_line(c_g, point, c_x, c_y, c_z, c_i, c_j, c_k, c_r)

        terminal.insert('end', '\n')
    terminal.config(state='disabled')
    root.update()
        

# 清空
def clear():
    code_text.delete('1.0', 'end')
    terminal.config(state='normal')
    terminal.delete('1.0', 'end')
    terminal.insert('1.0', '终端 Terminal\n')
    terminal.config(state='disabled')
    canvas.delete('all')
    canvas.create_line(0,250, 500,250, fill='white', arrow='last')
    canvas.create_line(250,0, 250,500, fill='white', arrow='first')

# 导入文件
def import_code():
    
    pass

# 导出文件
def export_code():
    
    pass

root = tkinter.Tk()
root.title('数控编程可视化')
root.geometry('1000x510')
root.resizable(False, False)

# 画布
canvas = tkinter.Canvas(root, bg='#212830', width=500, height=500,relief='flat')
canvas.grid(column=0,row=0,rowspan=3)
canvas.create_line(0,250, 500,250, fill='white', arrow='last')
canvas.create_line(250,500, 250,0, fill='white', arrow='last')

# 代码框
scrollbar_v = tkinter.ttk.Scrollbar(root)
scrollbar_v.grid(column=5,row=0,sticky=('N','S'))
code_text = tkinter.Text(root, height=10, width=50, yscrollcommand=scrollbar_v.set)
code_text.grid(column=1,row=0,columnspan=4,sticky=('N','S'))
scrollbar_v.config(command=code_text.yview)

# 生成按钮
submit_button = tkinter.ttk.Button(root, text='生成',command=submit)
submit_button.grid(column=1,row=1)

# 清空按钮
clear_button = tkinter.ttk.Button(root, text='清空', command=clear)
clear_button.grid(column=2,row=1)

# 导入按钮
import_button = tkinter.ttk.Button(root, text='导入', command=import_code)
import_button.grid(column=3,row=1)

# 导出按钮
export_button = tkinter.ttk.Button(root, text='导出', command=export_code)
export_button.grid(column=4,row=1)

# 代码解释框
terminal = tkinter.Text(root, height=5, width=50, relief='flat')
terminal.insert('end', '终端 Terminal\n')
terminal.config(state='disabled')
terminal.grid(column=1,row=2,columnspan=4,sticky=('N','S'))


root.mainloop()

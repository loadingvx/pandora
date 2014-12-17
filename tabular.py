#!/usr/bin/env python
#encoding:utf-8


import sys


def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    return False


class Tabular(object):

    def __init__(self):
        self.rows      = []
        self.col_width = {}


    def row(self, row):
        str_row = {}
        for k in row:
            str_row[str(k).decode("UTF-8")] = str(row[k]).decode('UTF-8')
        self.rows.append(str_row)

        for h in str_row:
            current_wid = self.view_width(str_row[h])
            if h not in self.col_width:
                self.col_width[h] = self.view_width(h)
            if self.col_width[h] < current_wid:
                self.col_width[h] = current_wid

    def view_width(self, label):
        width = 0
        for e in label:
            if is_chinese(e):
                width += 2
            else:
                width += 1
        return width+1

    def unicode_cnt(self, ustring):
        cnt = 0
        for each in ustring:
            if is_chinese(each):
                cnt+= 1
        return cnt




    def simple_print(self, primary_key='', max_lines=-1):
        if not primary_key:
            primary_key = self.col_width.keys()[0]
        keys = self.col_width.keys()
        keys.sort()

        header = [primary_key]
        header.extend([col for col in keys if col != primary_key])
        print '\t'.join(header)

        line_cnt = 0
        for line in self.rows:
            if primary_key in self.col_width:
                if primary_key in line:
                    content = '%s\t'%(line[primary_key])
                else:
                    content = '\t'
            for k in keys:
                if k == primary_key:
                    continue
                if k in line:
                    content += '%s\t'%(line[k])
                else:
                    content += '\t'
            if line_cnt > max_lines and max_lines > 0:
                print 'top of %d lines'%(max_lines)
                return
            line_cnt+= 1
            print content[:-1].encode('UTF-8')


    def show_table_with_border(self, primary_key='', max_lines=-1):
        bar = ''
        content = ''
        if not primary_key:
            primary_key = self.col_width.keys()[0]

        content = '| %s'%(primary_key.ljust(self.col_width[primary_key]-self.unicode_cnt(primary_key)))
        bar+= '+-%s'%('-'*self.col_width[primary_key])

        keys = self.col_width.keys()
        keys.sort()
        for each in keys:
            if each == primary_key:
                continue
            bar+= '+-%s'%('-'*self.col_width[each])
            content += '| %s'%(each.ljust(self.col_width[each]-self.unicode_cnt(each)))
        bar+= "+"
        content += "|"
        print bar
        print content.encode('UTF-8')
        print bar

        line_cnt = 0
        for line in self.rows:
            if primary_key in self.col_width:
                if primary_key in line:
                    content = '| %s'%(line[primary_key].ljust(self.col_width[primary_key]- self.unicode_cnt(line[primary_key])))
                else:
                    content = '| %s'%(''.ljust(self.col_width[primary_key]))
            for k in keys:
                if k == primary_key:
                    continue
                if k in line:
                    content += '| %s'%(line[k].ljust(self.col_width[k]-self.unicode_cnt(line[k])))
                else:
                    content += '| %s'%(''.ljust(self.col_width[k]))
            content += '|'
            if line_cnt > max_lines and max_lines > 0:
                print bar
                print 'top of %d lines'%(max_lines)
                return
            line_cnt+= 1
            print content.encode('UTF-8')
        print bar



    def render(self, primary_key='', max_lines=-1, border=True):
        if border:
            self.show_table_with_border(primary_key, max_lines)
        else:
            self.simple_print(primary_key, max_lines)






if __name__ == "__main__":
    t = Tabular()
    t.row({        'name':'John',  'age':'28'})
    t.row({'id':2,                 'age':'29'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.row({'id':1, 'name':'Peter', 'age':'28'})
    t.render('id', border=False)
    t.render('id')





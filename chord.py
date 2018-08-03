# -*- coding: utf-8 -*-
from itertools import product
import scale
import board
import pprint
import logging; logging.basicConfig(level=logging.INFO)


chord_types = {
        'M':[4,3],
        'm':[3,4],
        'M7':[4,3,4],
        'm7':[3,4,3],
        'm7-5':[3,3,4],
        'sus2':[2,5],
        'sus4':[5,2],
        'M9':[4,3,4,3],
        'add9':[4,3,7],
        }



class Chord(object):
    
    def __init__(self,**kw):
        self.base = kw.get('base','G')
        self.type = kw.get('type','maj7')
        self.scales = []
        self.positions = []
        self._init()
        
        self.filters = {
                'OpenChords':1,
                'Barrechord':0,
                'inversion':0,
                'gap':5,
                'ignor':[]
                }
        
    def _init(self):
        std_sca = list(scale.DIATONIC_SCALE)
        ind = std_sca.index(self.base)
        self.scales.append(self.base)
        for itv in chord_types[self.type]:
            ind += itv
            if ind>11:
                ind %= 12
            self.scales.append(std_sca[ind])
        
        strings = board.Board().strings
        inds = []
        for string in strings:
            ind = []
            inds.append(ind)
            for i,s in enumerate(string):
                if s in self.scales:
                    ind.append([i,s])
        self.positions  = list(product(inds[0],inds[1],inds[2],inds[3],inds[4],inds[5]))
    
    def get_positions(self,**kw):
        filters = kw.get('filters',self.filters)
        logging.info('开始过滤，过滤对象为：{0}{1} filters：{2}'.format(self.base,self.type,filters))
        positions = list(self.positions)
        logging.info('初始个数为：'+str(len(positions)))
        
        if filters['OpenChords']:
            positions = list(filter(lambda p:min(p)[0]>0, positions))
            logging.info('已过滤掉开放和弦，过滤后个数：'+str(len(positions)))
        if filters['Barrechord']:
            positions = list(filter(lambda p:min(p)[0]==0, positions))
            logging.info('已过滤掉封闭和弦，过滤后个数：'+str(len(positions)))

        ignor = filters['ignor']
        ignor = set(ignor) 
        scales = set(self.scales)
        scales -= ignor
        logging.info('开始进行确保过滤，确保存在的音为：'+str(scales))
        positions = list(filter(lambda p:set([val[1] for val in p])==scales, positions))
        logging.info('已完成确保过滤，过滤后个数：'+str(len(positions)))

        gap = filters['gap']
        logging.info('开始进行gap过滤，gap为：'+str(gap))
        positions = list(filter(lambda p:max(p)[0]-min(p,key=lambda i:(i[0]==0,i[0]))[0]<gap, positions))
        logging.info('已完成gap过滤，过滤后个数：'+str(len(positions)))
        

        return positions
        
    def draw_pic(self):
        pass

    def gen_wavg(self,file_name):
        pass
    
        
    
if __name__ == '__main__':            
    options = {
            'OpenChords':0,
            'Barrechord':0,
            'inversion':0,
            'gap':4,
            'ignor':[]
            }
    Cm9 = Chord(base='C',type='add9')
    pprint.pprint(Cm9.get_positions(filters=options))
    print(Cm9.scales)


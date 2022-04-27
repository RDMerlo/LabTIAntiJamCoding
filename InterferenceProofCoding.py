# -*- coding: utf-8 -*-

# Подключаемые модули

import math
import numpy as np

# Константы
nMethodHamming = 0 # Код Хэмминга
tMethodHamming = 'Код Хэмминга (совершенный код)'
nMethodQuasiPerfect = 1 # Квазисовершенный код
tMethodQuasiPerfect = 'Квазисовершенный код'
# Список методов
listMethod = (tMethodHamming, tMethodQuasiPerfect)

sizeSymbol = 8 # Размер 1-го символ в битах

# Функции и классы

# Параметры кодирования
class clsCode:
    def __init__(self, nMethod, m=9, rk=3):
        self.nMethod = nMethod # Метод кодирования
        # Определим параметры m, n и r(k)
        # Если выбран Код Хэмминга
        if nMethod == nMethodHamming:
            self.rk = rk
            self.n = 2**rk -1
            self.m = self.n - rk
        # Если выбран Квазисовершенный код
        elif nMethod == nMethodQuasiPerfect:
            self.m = m
            self.n = 1
            while (2**self.n)/(self.n+1) < 2**m:
                self.n += 1
            self.rk = self.n - m
        # Определим матрицу M (n x r(k))
        self.M = np.zeros([self.n,self.rk], dtype=int)
        for i in range(self.n):
            j = i + 1
            for k in range(self.rk):
                if j % 2 != 0:
                    self.M[i,k] = 1
                j //= 2
        pass

    def makeCode(self,a):
        # Построим строку b
        b =[]
        # Индекс i - индекс в строке a
        i = 0
        # Индекс k - показатель степени 2
        k = 0
        # Индекс j - индекс в строке b
        for j in range(self.n):
            # Если позиция - степень 2,
            # то в ней будет контрольная сумма
            if j+1 == 2**k:
                b.append(None)
                k += 1
            # Иначе - копируем биты a
            else:
                b.append(a[i])
                i += 1
        # Найдем котрольные суммы
        for k in range(self.rk):
            # Индекс j - индекс в строке b
            j = 2**k - 1
            # Находим сумму
            b[j] = 0
            # s - сумма по модулю 2 (b + e) x M[:,k]
            for i in range(self.n):
                if (b[i] == None or i==j):
                    continue
                b[j] += b[i] * self.M[i, k]
                b[j] %= 2
        return b

    def makeError(self,b,e):
        # Построим строку c = b + e
        c =[]
        # Индекс j - индекс в строках b и e
        for j in range(self.n):
            c.append((b[j]+e[j]) % 2)
        return c

    def makeDeCode(self, c):
        # Найдем err = (b + e) x M
        err = 0
        # k - разряд
        for k in range(self.rk):
            # s - сумма по модулю 2 (b + e) x M[:,k]
            s = 0
            for j in range(self.n):
                s += c[j]*self.M[j,k]
                s %= 2
            err += s*(2**k)
        # Копируем строку (b + e) в строку b
        b = [bit for bit in c]
        # исправляя, если надо, k-тый бит
        if err in range(1,self.n+1):
            b[err-1] = 1 if c[err-1] == 0 else 0
        # Построим строку a
        a =[]
        # Индекс k - показатель степени 2
        k = 0
        # Индекс j - индекс в строке b
        for j in range(self.n):
            # Если позиция - степень 2,
            # в ней - контрольная сумма - пропускаем
            if j+1 == 2**k:
                k += 1
            # Иначе - копируем биты b
            else:
                a.append(b[j])
        return err, b, a
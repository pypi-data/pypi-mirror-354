import numpy as np

# -*- coding: utf-8 -*-
"""
munpy_ext — расширенная библиотека методов численного анализа.
Функции p1…p29 включают подробную теорию (описание, основная идея, алгоритм, преимущества, недостатки) и код.
Дополнительно есть list_topics() для списка тем.
"""

def list_topics():
    """
    Возвращает словарь категорий и соответствующих номеров функций.
    """
    return {
        "Методы решения нелинейных уравнений": [1,2,3,4,5,6],
        "Методы для систем нелинейных уравнений": [7,8,9,10],
        "Интерполяция и аппроксимация": [11,12,13],
        "Умножение матриц": [14,15],
        "Собственные значения и спектр": [16,17,18,19,20,21,22],
        "Численные методы для ОДУ": [23,24,25,26,27],
        "Преобразования Фурье": [28,29]
    }

# ------------------ Методы решения нелинейных уравнений ------------------

def p1():
    theory = """
## 1. Метод половинного деления (бисекции)

### Описание
Метод основан на теореме о промежуточных значениях: если непрерывная функция f(x) меняет знак на концах [a,b], на этом отрезке есть корень.

### Основная идея
На каждом шаге интервал делится пополам, и выбирается та половина, на концах которой сохраняется изменение знака.

### Алгоритм
1. Проверка: f(a)*f(b)<0.
2. Пока (b-a)/2 > tol:
   - c=(a+b)/2
   - Если f(c)==0 или (b-a)/2<tol, выход.
   - Если f(a)*f(c)<0, b=c, иначе a=c.
3. Возвратить c.

### Преимущества
- Гарантированная сходимость.
- Простота реализации.

### Недостатки
- Линейная скорость.
- Неприменимо к кратным корням.
"""
    code = """
```python
def bisection(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) >= 0:
        raise ValueError('f(a) и f(b) одного знака')
    for _ in range(max_iter):
        c = (a + b)/2
        if abs(f(c))<tol or (b-a)/2<tol:
            return c
        if f(a)*f(c)<0:
            b=c
        else:
            a=c
    return (a+b)/2
```"""
    return theory+code

def p2():
    theory = """
## 2. Метод дихотомии (экстремумы)

### Описание
Подобен бисекции, но ищет минимум или максимум унимодальной функции без производных.

### Основная идея
Вокруг центра отрезка проверяются две точки, сравниваются их значения, затем выбирается та часть, где экстремум.

### Алгоритм
1. Задать a,b,eps,tol.
2. Пока b-a>tol:
   - mid=(a+b)/2; x1=mid-eps; x2=mid+eps
   - Если f(x1)<f(x2), b=x2, иначе a=x1.
3. Возвратить (a+b)/2.

### Преимущества
- Не требует f'.
- Надежно для унимодальных функций.

### Недостатки
- Линейная скорость.
- Параметр eps влияет.
"""
    code = """
```python
def dichotomy_min(f, a, b, tol=1e-6, eps=1e-4):
    while b-a>tol:
        mid=(a+b)/2
        x1,x2=mid-eps,mid+eps
        if f(x1)<f(x2): b=x2
        else: a=x1
    return (a+b)/2
```"""
    return theory+code

def p3():
    theory = """
## 3. Метод простой итерации

### Описание
Преобразует f(x)=0 к x=φ(x), итерации x_{k+1}=φ(x_k).

### Основная идея
Функция φ должна быть сжимающей (|φ'|<1) для гарантии сходимости.

### Алгоритм
1. Выбрать φ, x0.
2. x_{k+1}=φ(x_k) до |x_{k+1}-x_k|<tol.

### Преимущества
- Нет потребности в производных f.
- Проста.

### Недостатки
- Требует удачного выбора φ.
- Линейная скорость.
"""
    code = """
```python
def fixed_point(phi, x0, tol=1e-6, max_iter=100):
    x=x0
    for _ in range(max_iter):
        x1=phi(x)
        if abs(x1-x)<tol: return x1
        x=x1
    raise RuntimeError('Не сошлось')
```"""
    return theory+code

def p4():
    theory = """
## 4. Метод Ньютона

### Описание
Итерационный метод квадратичной сходимости основан на касательных.

### Основная идея
x_{k+1}=x_k - f(x_k)/f'(x_k).

### Алгоритм
1. x0.
2. Повторять шаг Ньютона до |Δx|<tol.

### Преимущества
- Высокая скорость.

### Недостатки
- Нужна f'.
- Может расходиться.
"""
    code = """
```python
def newton(f, df, x0, tol=1e-7, max_iter=50):
    x=x0
    for _ in range(max_iter):
        fx,dfx=f(x),df(x)
        if abs(dfx)<1e-12: raise ZeroDivisionError
        x1=x-fx/dfx
        if abs(x1-x)<tol: return x1
        x=x1
    return x
```"""
    return theory+code

def p5():
    theory = """
## 5. Модифицированный метод Ньютона

### Описание
Производная считается один раз в x0, далее фиксирована.

### Основная идея
x_{k+1}=x_k - f(x_k)/f'(x0).

### Алгоритм
1. d0=f'(x0).
2. Итерации, как в Ньютоне, но с d0.

### Преимущества
- Меньше вычислений.

### Недостатки
- Линейная скорость.
"""
    code = """
```python
def modified_newton(f, df, x0, tol=1e-6, max_iter=50):
    d0=df(x0)
    if abs(d0)<1e-12: raise ZeroDivisionError
    x=x0
    for _ in range(max_iter):
        x1=x-f(x)/d0
        if abs(x1-x)<tol: return x1
        x=x1
    return x
```"""
    return theory+code

def p6():
    theory = """
## 6. Метод секущих

### Описание
Аппроксимация Ньютона с секущей вместо касательной.

### Основная идея
x_{k+1}=x_k - f(x_k)*(x_k-x_{k-1})/(f(x_k)-f(x_{k-1})).

### Алгоритм
1. x0,x1.
2. Итерации секущих до tol.

### Преимущества
- Не требует f'.

### Недостатки
- Не гарантирована сходимость.
"""
    code = """
```python
def secant(f, x0, x1, tol=1e-6, max_iter=50):
    for _ in range(max_iter):
        f0,f1=f(x0),f(x1)
        if abs(f1-f0)<1e-12: break
        x2=x1 - f1*(x1-x0)/(f1-f0)
        if abs(x2-x1)<tol: return x2
        x0,x1=x1,x2
    return x1
```"""
    return theory+code

# 2. Методы для систем нелинейных уравнений (p7–p10)

def p7():
    theory = """
## 7. Метод функциональной итерации для систем

### Описание
Обобщение метода простой итерации на векторные функции: решаем F(X)=0, переписывая как X=G(X).

### Основная идея
Система уравнений представляется в виде неподвижного отображения G: X_{k+1}=G(X_k).

### Алгоритм
1. Выбрать G и начальное приближение X0.
2. Пока ||X_{k+1}-X_k||>tol:
   - X_{k+1}=G(X_k).
3. Вернуть X_{k+1}.

### Преимущества
- Простота.
- Нет необходимости в Якобиане.

### Недостатки
- Линейная скорость.
- Требует ||J_G||<1.
"""
    code = """
```python
def fixed_point_system(G, X0, tol=1e-6, max_iter=100):
    X = np.array(X0, float)
    for _ in range(max_iter):
        X1 = np.array([g(*X) for g in G])
        if np.linalg.norm(X1-X) < tol:
            return X1
        X = X1
    raise RuntimeError('Не сошлось')
```"""
    return theory+code


def p8():
    theory = """
## 8. Метод Гаусса–Зейделя

### Описание
Модификация функциональной итерации: каждая компонента x_i обновляется сразу с учётом новых значений предыдущих компонент.

### Основная идея
Использовать результаты текущей итерации для ускорения сходимости.

### Алгоритм
1. Задать X0.
2. Для k в 1..max_iter:
   - Для i в 1..n:
       x_i^{(k+1)} = g_i(x_1^{(k+1)},...,x_{i-1}^{(k+1)}, x_i^{(k)},...,x_n^{(k)}).
   - Если ||X^{(k+1)}-X^{(k)}||<tol, выход.

### Преимущества
- Быстрее простой итерации.

### Недостатки
- Требует диагонального преобладания для гарантии.
"""
    code = """
```python
def gauss_seidel(G, X0, tol=1e-6, max_iter=100):
    X = list(X0)
    n = len(G)
    for _ in range(max_iter):
        X_old = X.copy()
        for i, g in enumerate(G):
            X[i] = g(*X)
        if np.linalg.norm(np.array(X)-np.array(X_old)) < tol:
            return np.array(X)
    raise RuntimeError('Не сошлось')
```"""
    return theory+code


def p9():
    theory = """
## 9. Метод Ньютона для систем

### Описание
Итерационный метод с квадратичной сходимостью для векторных уравнений F(X)=0, использующий Якобиан.

### Основная идея
На каждом шаге решается линейная система J(X_k) ΔX = -F(X_k), обновляется X_{k+1}=X_k+ΔX.

### Алгоритм
1. X0, tol.
2. Пока ||ΔX||>tol:
   - Вычислить F, J;
   - ΔX = solve(J, -F);
   - X = X + ΔX.

### Преимущества
- Квадратичная сходимость.

### Недостатки
- Требует построения и решения системы с J.
"""
    code = """
```python
def newton_system(F, J, X0, tol=1e-6, max_iter=20):
    X = np.array(X0, float)
    for _ in range(max_iter):
        Fv = np.array(F(X))
        Jv = np.array(J(X))
        delta = np.linalg.solve(Jv, -Fv)
        X = X + delta
        if np.linalg.norm(delta) < tol:
            return X
    raise RuntimeError('Не сошлось')
```"""
    return theory+code


def p10():
    theory = """
## 10. Модифицированный метод Ньютона для систем

### Описание
Якобиан вычисляется один раз в X0, затем используется повторно, что снижает порядок до линейного.

### Основная идея
J0=J(X0), на каждой итерации решаем J0 ΔX = -F(X_k).

### Алгоритм
1. X0, J0.
2. Пока ||ΔX||>tol:
   - ΔX = solve(J0, -F(X_k));
   - X_{k+1} = X_k + ΔX.

### Преимущества
- Экономия на вычислении J.

### Недостатки
- Линейная сходимость.
"""
    code = """
```python
def modified_newton_system(F, J, X0, tol=1e-6, max_iter=20):
    X = np.array(X0, float)
    J0 = np.array(J(X))
    for _ in range(max_iter):
        Fv = np.array(F(X))
        delta = np.linalg.solve(J0, -Fv)
        X = X + delta
        if np.linalg.norm(delta) < tol:
            return X
    raise RuntimeError('Не сошлось')
```"""
    return theory+code


# 3. Интерполяция и аппроксимация (p11–p13)

def p11():
    theory = """
## 11. Линейная интерполяция

### Описание
Кусочно-линейная аппроксимация: на каждом отрезке [x_i, x_{i+1}] строится прямая через (x_i,y_i) и (x_{i+1},y_{i+1}).

### Основная идея
Использовать прямую, задающуюся двумя точками, для оценки внутри отрезка.

### Алгоритм
1. Найти i такое, что x ∈ [x_i, x_{i+1}].
2. y = y_i + (y_{i+1}-y_i)/(x_{i+1}-x_i)*(x-x_i).

### Преимущества
- Простота.
- Локальная зависимость.

### Недостатки
- Непрерывна, но не гладка в узлах.
"""
    code = """
```python
def linear_interp(x_vals, y_vals, x):
    for i in range(len(x_vals)-1):
        if x_vals[i] <= x <= x_vals[i+1]:
            x0, x1 = x_vals[i], x_vals[i+1]
            y0, y1 = y_vals[i], y_vals[i+1]
            return y0 + (y1-y0)*(x-x0)/(x1-x0)
    raise ValueError('x вне диапазона')
```"""
    return theory+code


def p12():
    theory = """
## 12. Интерполяционный многочлен Лагранжа

### Описание
Глобальный многочлен степени n, проходящий через n+1 узлов.

### Основная идея
Использовать базисные полиномы l_i(x), где l_i(x_j)=δ_{ij}.

### Алгоритм
L(x)=Σ_{i=0}^n y_i Π_{j≠i} (x-x_j)/(x_i-x_j).

### Преимущества
- Эксплицитная формула.

### Недостатки
- Феномен Рунге при больших n.
"""
    code = """
```python
def lagrange(x_vals, y_vals, x):
    total=0
    n=len(x_vals)
    for i in range(n):
        term=y_vals[i]
        for j in range(n):
            if i!=j:
                term *= (x - x_vals[j])/(x_vals[i]-x_vals[j])
        total += term
    return total
```"""
    return theory+code

def p13():
    theory = """
## 13. Кубическая сплайн-интерполяция

### Описание
Кусочно-кубические полиномы, обеспечивающие непрерывность функции и её первой и второй производных.

### Основная идея
Решить трёхдиагональную систему для вторых производных и построить сплайн по формуле S_i(x).

### Алгоритм
1. Вычислить h_i и составить систему для c_i.
2. Решить прогонкой.
3. Найти a,b,c,d коэффициенты.
4. Оценить S(x).

### Преимущества
- Гладкость C^2.

### Недостатки
- Сложнее реализации.
"""
    code = """
```python
def cubic_spline_coeffs(x, y):
    n=len(x)-1
    h=[x[i+1]-x[i] for i in range(n)]
    al=[3*(y[i+1]-y[i])/h[i]-3*(y[i]-y[i-1])/h[i-1] for i in range(1,n)]
    l=[1]+[0]*n; mu=[0]*(n+1); z=[0]*(n+1)
    for i in range(1,n):
        l[i]=2*(x[i+1]-x[i-1]) - h[i-1]*mu[i-1]
        mu[i]=h[i]/l[i]
        z[i]=(al[i-1]-h[i-1]*z[i-1])/l[i]
    l[n]=1; z[n]=0; c=[0]*(n+1)
    b=[0]*n; d=[0]*n; a=y[:n]
    for j in range(n-1,-1,-1):
        c[j]=z[j]-mu[j]*c[j+1]
        b[j]=(y[j+1]-y[j])/h[j] - h[j]*(c[j+1]+2*c[j])/3
        d[j]=(c[j+1]-c[j])/(3*h[j])
    return a,b,c,d

def cubic_spline(x, y, x0):
    a,b,c,d = cubic_spline_coeffs(x,y)
    for i in range(len(x)-1):
        if x[i]<=x0<=x[i+1]:
            dx=x0-x[i]
            return a[i]+b[i]*dx+c[i]*dx**2+d[i]*dx**3
    raise ValueError('x вне диапазона')
```"""
    return theory+code

# 4. Умножение матриц (p14–p15)

def p14():
    theory = """
## 14. Наивное перемножение матриц

### Описание
Тройной цикл: C_{ij}=Σ_k A_{ik}*B_{kj}.

### Основная идея
Прямое применение определения умножения матриц.

### Алгоритм
1. Инициализировать C нулями.
2. Тройной цикл по i,j,k.

### Преимущества
- Простая реализация.

### Недостатки
- O(n^3), медленно для больших n.
"""
    code = """
```python
def matmul_naive(A, B):
    m, p = len(A), len(B[0])
    n = len(B)
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k]*B[k][j]
    return C
```"""
    return theory+code

def p15():
    theory = """
## 15. Алгоритм Штрассена

### Описание
Рекурсивное «разделяй и властвуй»: для квадратных матриц размером степень 2.

### Основная идея
Вычислить 7 продуктов P1..P7 вместо 8, комбинировать блоки.

### Алгоритм
1. Базовый случай n<=2 – наивное умножение.
2. Разбить на подматрицы.
3. Вычислить P1..P7.
4. Скомбинировать C11..C22.

### Преимущества
- O(n^{2.807}), быстрее O(n^3).

### Недостатки
- Сложнее, требует степени двойки.
"""
    code = """
```python
def strassen(A, B):
    n = A.shape[0]
    if n <= 2:
        return A.dot(B)
    m = n//2
    A11,A12 = A[:m,:m],A[:m,m:]
    A21,A22 = A[m:,:m],A[m:,m:]
    B11,B12 = B[:m,:m],B[:m,m:]
    B21,B22 = B[m:,:m],B[m:,m:]
    P1 = strassen(A11+A22, B11+B22)
    P2 = strassen(A21+A22, B11)
    P3 = strassen(A11, B12-B22)
    P4 = strassen(A22, B21-B11)
    P5 = strassen(A11+A12, B22)
    P6 = strassen(A21-A11, B11+B12)
    P7 = strassen(A12-A22, B21+B22)
    C11 = P1+P4-P5+P7
    C12 = P3+P5
    C21 = P2+P4
    C22 = P1-P2+P3+P6
    top = np.hstack((C11,C12))
    bot = np.hstack((C21,C22))
    return np.vstack((top,bot))
```"""
    return theory+code

# 5. Собственные значения и спектр (p16–p22)

def p16():
    theory = """
## 16. Характеристический многочлен (2×2)

### Описание
Аналитический метод: решает det(A-λI)=0 для 2×2.

### Основная идея
Характеристический многочлен λ^2 - tr(A)λ + det(A)=0.

### Алгоритм
1. Вычислить tr, det.
2. Решить квадратное уравнение.

### Преимущества
- Точное решение для 2×2.

### Недостатки
- Не масштабируется на большие матрицы.
"""
    code = """
```python
import cmath

def char_poly_2(A):
    tr = A[0,0]+A[1,1]
    det = A[0,0]*A[1,1]-A[0,1]*A[1,0]
    disc = tr*tr-4*det
    return ((tr+cmath.sqrt(disc))/2, (tr-cmath.sqrt(disc))/2)
```"""
    return theory+code

def p17():
    theory = """
## 17. Степенной метод

### Описание
Итерационный метод для нахождения доминантного собственного значения и вектора.

### Основная идея
x_{k+1}=A x_k / ||A x_k||, λ≈||A x_k||.

### Алгоритм
1. Выбрать x0.
2. y=A x_k; λ=||y||; x_{k+1}=y/λ до сходимости.

### Преимущества
- Хорош для разреженных матриц.

### Недостатки
- Находит только наибольшее по модулю λ.
"""
    code = """
```python
def power_iteration(A, tol=1e-6, max_iter=1000):
    b = np.random.rand(A.shape[1])
    for _ in range(max_iter):
        b1 = A.dot(b)
        lam = np.linalg.norm(b1)
        b1 /= lam
        if np.linalg.norm(b1-b)<tol: return lam,b1
        b = b1
    return lam,b
```"""
    return theory+code

def p18():
    theory = """
## 18. Обратная итерация (со сдвигом)

### Описание
Позволяет искать λ близкие к σ через решение (A-σI) y = x.

### Основная идея
y нормируется, λ=1/||y||+σ.

### Алгоритм
1. M=A-σI.
2. Для k: y=solve(M,x_k); μ=||y||; x_{k+1}=y/μ; λ=1/μ+σ.

### Преимущества
- Ищет произвольный λ.

### Недостатки
- Требует решения лин. системы.
"""
    code = """
```python
def inverse_iteration(A, sigma, tol=1e-6, max_iter=100):
    n=A.shape[0]; M=A-sigma*np.eye(n); x=np.random.rand(n)
    lam_old=0
    for _ in range(max_iter):
        y=np.linalg.solve(M,x)
        mu=np.linalg.norm(y); x=y/mu
        lam=1/mu+sigma
        if abs(lam-lam_old)<tol: return lam,x
        lam_old=lam
    return lam,x
```"""
    return theory+code

def p19():
    theory = """
## 19. Метод вращений Якоби

### Описание
Итерационно зануляет максимальные внедиагональные элементы через ортогональные вращения.

### Основная идея
Использует матрицы Гивенса для преобразования подобия.

### Алгоритм
1. Найти i,j макс внедиаг.
2. Вычислить угол φ, построить R.
3. A←R^T A R; повторять.

### Преимущества
- Сходим для симметричных A.

### Недостатки
- Медленнее QR.
"""
    code = """
```python
def jacobi(A, tol=1e-9, max_iter=100):
    A=A.astype(float); n=A.shape[0]; V=np.eye(n)
    for _ in range(max_iter):
        i,j=np.unravel_index(np.argmax(np.abs(A-np.diag(np.diag(A)))),A.shape)
        if abs(A[i,j])<tol: break
        phi=0.5*np.arctan2(2*A[i,j],A[j,j]-A[i,i])
        c,s=np.cos(phi),np.sin(phi)
        R=np.eye(n); R[i,i]=c; R[j,j]=c; R[i,j]=s; R[j,i]=-s
        A=R.T.dot(A).dot(R); V=V.dot(R)
    return np.diag(A),V
```"""
    return theory+code

def p20():
    theory = """
## 20. QR-алгоритм

### Описание
Итерационное разложение A_k=Q_kR_k, затем A_{k+1}=R_kQ_k.

### Основная идея
При сходимости A→T треугольная, diag(T)=λ.

### Алгоритм
1. A0=A.
2. Q,R=qr(A_k);
   A_{k+1}=R Q.
3. Повторять до max_iter.

### Преимущества
- Универсален.

### Недостатки
- O(n^3).
"""
    code = """
```python
def qr_eigenvalues(A, max_iter=100):
    A_k=A.copy().astype(float)
    for _ in range(max_iter):
        Q,R=np.linalg.qr(A_k)
        A_k=R.dot(Q)
    return np.diag(A_k)
```"""
    return theory+code

def p21():
    theory = """
## 21. Разложение Шура

### Описание
Любую квадратную A можно представить как Q^*AQ=T, где T верхнетреугольная.

### Основная идея
Использовать QR-алгоритм или специальные процедуры из лин. алгебры.

### Алгоритм
Вызов scipy.linalg.schur или аналог.

### Преимущества
- Численно устойчиво.

### Недостатки
- Требует специализированных библиотек.
"""
    code = """
```python
def schur(A):
    from scipy.linalg import schur
    T,Q=schur(A)
    return T,Q
```"""
    return theory+code

def p22():
    theory = """
## 22. QR-разложение

### Описание
A=Q R, Q ортонормированная, R верхнетреугольная.

### Основная идея
Использовать Гивенсовы или Хаусхолдеры.

### Алгоритм
Вызов np.linalg.qr или вручную.

### Преимущества
- Быстро и надёжно.

### Недостатки
- O(n^3).
"""
    code = """
```python
def qr_decomp(A):
    return np.linalg.qr(A)
```"""
    return theory+code

# 6. Численные методы для ОДУ (p23–p27)

def p23():
    theory = """
## 23. Явный метод Эйлера

### Описание
Наивный метод конечных разностей первого порядка для y'=f(t,y).

### Основная идея
Приближать производную прямым шагом: y_{n+1}=y_n+h f(t_n,y_n).

### Алгоритм
1. t0,y0,h,n
2. Для i в 0..n-1: y+=h*f(t,y); t+=h.

### Преимущества
- Прост

### Недостатки
- Низкий порядок, нестабилен для жёстких ОДУ.
"""
    code = """
```python
def euler(f,t0,y0,h,n):
    t,y=t0,y0; sol=[(t,y)]
    for _ in range(n):
        y=y+h*f(t,y); t=t+h; sol.append((t,y))
    return sol
```"""
    return "theory+code"

def p24():
    theory = """
## 24. Предиктор-корректор Эйлера

### Описание
Двухшаговый метод: сначала предиктор (явный), затем корректировка.

### Основная идея
Использовать среднее значение наклона.

### Алгоритм
1. y_pred=y_n+h f(t_n,y_n)
2. y_{n+1}=y_n+h/2[f(t_n,y_n)+f(t_{n+1},y_pred)]

### Преимущества
- Более точен, чем Эйлер.

### Недостатки
- Требует дополнительного вызова f.
"""
    code = """
```python
def euler_pc(f,t0,y0,h,n):
    t,y=t0,y0; sol=[(t,y)]
    for _ in range(n):
        y_pred=y+h*f(t,y)
        t_new=t+h
        y=y+h*(f(t,y)+f(t_new,y_pred))/2
        t=t_new; sol.append((t,y))
    return sol
```"""
    return theory+code


def p25():
    theory = """
## 25. Метод Рунге–Кутты 4-го порядка

### Описание
Классический RK4 с четвёртым порядком точности.

### Основная идея
Комбинация четырёх оценок наклона k1..k4.

### Алгоритм
k1=f(t_n,y_n)
... (см. код)

### Преимущества
- Высокая точность, устойчивость.

### Недостатки
- Четыре вычисления f.
"""
    code = """
```python
def rk4(f,t0,y0,h,n):
    t,y=t0,y0; sol=[(t,y)]
    for _ in range(n):
        k1=f(t,y)
        k2=f(t+h/2,y+h*k1/2)
        k3=f(t+h/2,y+h*k2/2)
        k4=f(t+h,y+h*k3)
        y=y+h*(k1+2*k2+2*k3+k4)/6
        t+=h; sol.append((t,y))
    return sol
```"""
    return theory+code


def p26():
    theory = """
## 26. Метод Адамса–Башфорта (2 шага)

### Описание
Явный многошаговый метод второго порядка.

### Основная идея
Использует f_n и f_{n-1}.

### Алгоритм
y_{n+1}=y_n+h/2(3f_n-f_{n-1}).

### Преимущества
- Меньше вызовов f.

### Недостатки
- Требует двух стартовых значений.
"""
    code = """
```python
def adams_bashforth2(f,ts,ys,h):
    sol=ys[:2]
    for i in range(1,len(ts)-1):
        sol.append(sol[i]+h*(3*f(ts[i],sol[i])-f(ts[i-1],sol[i-1]))/2)
    return sol
```"""
    return theory+code


def p27():
    theory = """
## 27. Метод Адамса–Мултона (2 шага)

### Описание
Неявный многошаговый метод второго порядка.

### Основная идея
Использует f_{n+1}, требует решения уравнения.

### Алгоритм
y_{n+1}=y_n+h/12(5f_{n+1}+8f_n-f_{n-1}).

### Преимущества
- Более высокая точность и устойчивость.

### Недостатки
- Неявный: требует решения.
"""
    code = """
```python
def adams_moulton2(f,ts,ys,h):
    sol=ys[:2]
    for i in range(1,len(ts)-1):
        y_pred=sol[i]+h*f(ts[i],sol[i])
        sol.append(sol[i]+h*(5*f(ts[i+1],y_pred)+8*f(ts[i],sol[i])-f(ts[i-1],sol[i-1]))/12)
    return sol
```"""
    return theory+code


# 7. Преобразования Фурье (p28–p29)

def p28():
    theory = """
## 28. Дискретное преобразование Фурье (DFT)

### Описание
Переводит дискретный сигнал x_n в спектр X_k.

### Основная идея
X_k = Σ_{n=0..N-1} x_n e^{-2πi k n/N}, обратное x_n=1/N Σ X_k e^{2πi k n/N}.

### Алгоритм
Прямое вычисление сумм за O(N^2).

### Преимущества
- Понятная формула.

### Недостатки
- O(N^2).
"""
    code = """
```python
def dft(x):
    N=len(x)
    return [sum(x[n]*np.exp(-2j*np.pi*k*n/N) for n in range(N)) for k in range(N)]

def idft(X):
    N=len(X)
    return [sum(X[k]*np.exp(2j*np.pi*k*n/N) for k in range(N))/N for n in range(N)]
```"""
    return theory+code


def p29():
    theory = """
## 29. Быстрое преобразование Фурье (FFT)

### Описание
Рекурсивный алгоритм DFT за O(N log N) через деление на чётные/нечётные.

### Основная идея
Разбить вход на две половины, рекурсивно вычислить FFT, объединить.

### Алгоритм
1. Если N<=1, вернуть x.
2. even=fft(x[0::2]), odd=fft(x[1::2]).
3. T_k=exp(-2πi k/N)*odd[k]; результат=[even[k]+T_k, even[k]-T_k].

### Преимущества
- O(N log N).

### Недостатки
- Требует N степень двойки для простоты.
"""
    code = """
```python
def fft(x):
    N=len(x)
    if N<=1: return x
    even=fft(x[0::2])
    odd=fft(x[1::2])
    T=[np.exp(-2j*np.pi*k/N)*odd[k] for k in range(N//2)]
    return [even[k]+T[k] for k in range(N//2)] + [even[k]-T[k] for k in range(N//2)]
```"""
    return theory+code


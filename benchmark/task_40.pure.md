
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--scaleFloat

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => T2 -> a -> a
```   

# code
```haskell
f1 0 x      = x
f1 0 x      = x
f1 0 x      = x
f1 k x
      | isFix       =  x
      | otherwise   =  f2 m (n + f3 b k)
      where (m,n) = f4 x
            (l,h) = f5 x
            d     = f6 x
            b     = h - l + 4*d
            isFix = x == 0 || f7 x || f8 x
```

# dependencies
## 0
```haskell
f6 :: T1 a => a -> T2
```
## 1
```haskell
f5 :: T1 a => a -> (T2,T2)
```
## 3
```haskell
(*) :: T4 a => a -> a -> a
```
## 4
```haskell
(+) :: T4 a => a -> a -> a
```
## 6
```haskell
f8 :: T1 a => a -> T6
```
## 7
```haskell
f2 :: T1 a => T3 -> T2 -> a
```
## 8
```haskell
f3 :: (T5 a) => (a, a) -> a -> a
```
## 9
```haskell
f4 :: T1 a =>  a -> (T3,T2)
```
## 10
```haskell
f7 :: T1 a => a -> T6
```

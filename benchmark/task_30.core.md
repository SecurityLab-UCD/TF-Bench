
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--round

# poly_type
Ad-hoc

# signature
```haskell
round :: (RealFrac a, Integral b) => a -> b
```   

# code
```haskell
round x             =  let (n,r) = properFraction x
                               m     = if r < 0 then n - 1 else n + 1
                           in case signum (abs r - 0.5) of
                                -1 -> n
                                0  -> if even n then n else m
                                1  -> m
                                _  -> error "Bad value"
```

# dependencies
## 0
```haskell
properFraction :: (RealFrac a, Integral b) => a -> (b, a)
```
## 1
```haskell
abs :: Num a => a -> a
```
## 2
```haskell
(+) :: Num a => a -> a -> a
```
## 3
```haskell
(-) :: Num a => a -> a -> a
```
## 4
```haskell
signum :: Num a => a -> a
```
## 5
```haskell
even :: Integral a => a -> Bool
```

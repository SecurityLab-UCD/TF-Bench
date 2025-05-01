
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--properFraction

# poly_type
Ad-hoc

# signature
```haskell
properFraction :: (RealFrac a, Integral b) => a -> (b,a)
```   

# code
```haskell
properFraction (x:%y) = (fromInteger (toInteger q), r:%y)
  where (q,r) = quotRem x y
```

# dependencies
## 0
```haskell
quotRem :: Integral a => a -> a -> (a,a)
```
## 1
```haskell
toInteger :: Integral => a -> Integer
```
## 2
```haskell
fromInteger :: Integral => Integer -> a
```
## 3
```haskell
data  Ratio a = !a :% !a
```
## 4
```haskell
type  Rational = Ratio Integer
```



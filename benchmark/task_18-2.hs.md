
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--toRational-Integer

# poly_type
Monomorphic

# signature
```haskell
toRational :: Integer -> Rational
```   

# code
```haskell
toRational x =  x :% one
```

# dependencies
## 0
```haskell
one :: Integer
```
## 1
```haskell
data  Ratio a = !a :% !a
```
## 2
```haskell
type  Rational =  Ratio Integer
```



# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--toRational-Natural

# poly_type
Monomorphic

# signature
```haskell
toRational :: Natural -> Rational
```   

# code
```haskell
toRational n = integerFromNatural n :% 1
```

# dependencies
## 0
```haskell
integerFromNatural :: Natural -> Integer
```
## 1
```haskell
(:%) :: Integer -> Integer -> Rational
```

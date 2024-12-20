
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
toRational x =  x :% 1
```

# dependencies
## 0
```haskell
(:%) :: Integer -> Integer -> Rational
```

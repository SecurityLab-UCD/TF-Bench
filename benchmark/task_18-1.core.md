
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--toRational-Int

# poly_type
Monomorphic

# signature
```haskell
toRational :: Int -> Rational
```   

# code
```haskell
toRational x        =  toInteger x :% 1
```

# dependencies
## 0
```haskell
toInteger :: Int -> Integer
```
## 1
```haskell
(:%) :: Integer -> Integer -> Rational
```

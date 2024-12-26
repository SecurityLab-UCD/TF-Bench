
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
toRational x = toInteger x :% one
```

# dependencies
## 0
```haskell
toInteger :: Int -> Integer
```
## 1
```haskell
one :: Integer
```
## 2
```haskell
data  Ratio a = !a :% !a
```
## 3
```haskell
type  Rational          =  Ratio Integer
```


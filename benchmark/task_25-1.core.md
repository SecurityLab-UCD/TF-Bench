
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--toInteger--Natural

# poly_type
Monomorphic

# signature
```haskell
toInteger :: Natural -> Integer
```   

# code
```haskell
toInteger x = integerFromNatural x
```

# dependencies
## 0
```haskell
integerFromNatural :: Natural -> Integer
```
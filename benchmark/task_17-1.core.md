
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--fromInteger-Int

# poly_type
Monomorphic

# signature
```haskell
fromInteger :: Integer -> Int
```   

# code
```haskell
fromInteger i = I# (integerToInt# i)
```

# dependencies
## 0
```haskell
integerToInt# :: Integer -> Int#
```
## 1
```haskell
I# :: Int# -> Int
```


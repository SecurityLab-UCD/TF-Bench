
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
fromInteger i = I_ (integerToInt_ i)
```

# dependencies
## 0
```haskell
integerToInt_ :: Integer -> Int_
```
## 1
```haskell
data Int = I_ Int_
```



# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--encodeFloat-Float

# poly_type
Monomorphic

# signature
```haskell
encodeFloat :: Integer -> Int -> Float
```   

# code
```haskell
encodeFloat i (I_ e) = F_ (integerEncodeFloat_ i e)
```

# dependencies
## 0
```haskell
data Int = I_ Int_
```
## 1
```haskell
data Float = F_ Float_
```
## 2
```haskell
integerEncodeFloat_ :: Integer -> Int_ -> Float_
```
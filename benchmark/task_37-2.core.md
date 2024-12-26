
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--encodeFloat-Double

# poly_type
Monomorphic

# signature
```haskell
encodeFloat :: Integer -> Int -> Double
```   

# code
```haskell
encodeFloat i (I_ j) = D_ (integerEncodeDouble_ i j)
```

# dependencies
## 0
```haskell
data Double = D_ Double_
```
## 1
```haskell
integerEncodeDouble_ :: Integer -> Int_ -> Double_
```
## 2
```haskell
data Int = I_ Int_
```
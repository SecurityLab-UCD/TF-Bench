
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--decodeFloat-Double

# note
modified

# poly_type
Monomorphic

# signature
```haskell
decodeFloat :: Double -> (Integer, Int)
```   

# code
```haskell
decodeFloat (D_ x_) = case integerDecodeDouble_ x_   of
                      (i, j) -> (i, I_ j)
```

# dependencies
## 0
```haskell
data Double = D_ Double_
```
## 1
```haskell
integerDecodeDouble_ :: Double_ -> (Integer, Int_)
```
## 2
```haskell
data Int = I_ Int_
```
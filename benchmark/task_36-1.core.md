
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--decodeFloat-Float

# poly_type
Monomorphic

# note
modified

# signature
```haskell
decodeFloat :: Float -> (Integer, Int)
```   

# code
```haskell
decodeFloat (F f) = case decodeFloat_Int_ f_ of
                      (i, e) -> (IS i, I e)
```

# dependencies
## 0
```haskell
data Float = F_ Float_
```
## 1
```haskell
decodeFloat_Int_ :: Float_ -> (Int_, Int_)
```
## 2
```haskell
data Integer = IS Int_
```
## 3
```haskell
data Int = I_ Int_
```
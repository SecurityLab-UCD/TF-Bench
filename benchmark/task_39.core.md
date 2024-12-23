
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--significand

# poly_type
Ad-hoc

# signature
```haskell
significand :: RealFloat a => a -> a
```   

# code
```haskell
significand x = encodeFloat m (negate (floatDigits x))
    where (m,_) = decodeFloat x
```

# dependencies
## 0
```haskell
encodeFloat :: RealFloat a => Integer -> Int -> a
```
## 1
```haskell
decodeFloat :: RealFloat a => a -> (Integer, Int)
```
## 2
```haskell
floatDigits :: RealFloat a => a -> Int
```
## 3
```haskell
negate :: Num a => a -> a
```
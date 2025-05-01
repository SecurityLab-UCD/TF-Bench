
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--rem

# poly_type
Ad-hoc

# signature
```haskell
rem :: Integral a => a -> a -> a
```   

# code
```haskell
n `rem` d = snd (quotRem n d)
```

# dependencies
## 0
```haskell
snd :: (a, b) -> b
```
## 1
```haskell
quotRem :: Integral a => a -> a -> (a, a)
```

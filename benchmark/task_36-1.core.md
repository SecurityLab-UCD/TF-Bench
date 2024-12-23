
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--decodeFloat-Float

# poly_type
Monomorphic

# signature
```haskell
decodeFloat :: Float -> (Integer, Int)
```   

# code
```haskell
decodeFloat (F# f#) = case decodeFloat_Int# f# of
                      (# i, e #) -> (IS i, I# e)
```

# dependencies
## 0
```haskell
F# :: Float# -> Float
```
## 1
```haskell
decodeFloat_Int# :: Float# -> (# Int#, Int# #)
```
## 2
```haskell
IS :: Int# -> Integer
```
## 3
```haskell
I# :: Int# -> Int
```
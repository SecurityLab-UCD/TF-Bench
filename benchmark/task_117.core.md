
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--putChar

# poly_type
Monomorphic

# signature
```haskell
putChar :: Char -> IO ()
```   

# code
```haskell
putChar c =  hPutChar stdout c
```

# dependencies
## 0
```haskell
hPutChar :: Handle -> Char -> IO ()
```
## 1
```haskell
stdout :: Handle
```
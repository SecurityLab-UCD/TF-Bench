
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--putStr

# poly_type
Monomorphic

# signature
```haskell
putStr :: String -> IO ()
```   

# code
```haskell
putStr s =  hPutStr stdout s
```

# dependencies
## 0
```haskell
hPutStr :: Handle -> String -> IO ()
```
## 1
```haskell
stdout :: Handle
```

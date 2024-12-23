
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--putStrLn

# poly_type
Monomorphic

# signature
```haskell
putStrLn :: String -> IO ()
```   

# code
```haskell
putStrLn s =  hPutStrLn stdout s
```

# dependencies
## 0
```haskell
hPutStrLn :: Handle -> String -> IO ()
```
## 1
```haskell
stdout :: Handle
```

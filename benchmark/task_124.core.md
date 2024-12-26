
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/System/IO.hs--appendFile

# poly_type
Monomorphic

# signature
```haskell
appendFile :: FilePath -> String -> IO ()
```   

# code
```haskell
appendFile f txt = withFile f AppendMode (\ hdl -> hPutStr hdl txt)
```

# dependencies
## 0
```haskell
hPutStr :: Handle -> String -> IO ()
```
## 1
```haskell
withFile :: FilePath -> IOMode -> (Handle -> IO r) -> IO r
```
## 2
```haskell
data IOMode = ReadMode | WriteMode | AppendMode | ReadWriteMode
```


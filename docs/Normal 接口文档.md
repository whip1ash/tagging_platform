# Normal 接口列表

### 1. sentence_list

1. 请求域名：/Sentence/List
2. 输入参数：

```json
{
    "page":int,
    "limit":int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "List sentences success!", 
    "code": 0, 
    "data": [
        {
            "id": int,
            "content": string,
            "source": char,
            "entity_tag": bool,
            "relation_tag": bool
        }
    ]
}
```

4. 错误码

   | Error          | Code | Description                        |
   | -------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE | 998  | This api only support post method! |
   | DATABASE_ERROR | 3    | List all sentence failed           |

### 2. sentence_done

1. 请求域名：/Sentence/Done
2. 输入参数：

```json
{
    "referer": string, entity
    "page": int, 0 
    "limit": int 10
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "List done sentences success!", 
    "code": 0, 
    "data": [
        {
            "id": int,
            "content": string,
            "source": char,
            "entity_tag": bool,
            "relation_tag": bool
        }
    ]
}
```

4. 错误码

   | Error          | Code | Description                        |
   | -------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE | 998  | This api only support post method! |
   | DATABASE_ERROR | 3    | List done sentence failed          |

### 3. sentence_doing

1. 请求域名：/Sentence/Doing
2. 输入参数：

```json
{
    "referer":string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "List doing sentences success!", 
    "code": 0, 
    "data": [
        {
            "id": int,
            "content": string,
            "source": char,
            "entity_tag": bool,
            "relation_tag": bool
        }
    ]
}
```

4. 错误码

   | Error            | Code | Description                        |
   | ---------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE   | 998  | This api only support post method! |
   | DATABASE_ERROR   | 3    | List doing sentence failed         |
   | WRONG_PARAM_CODE | 2    | Input a invalid referer            |

### 4. sentence_count

1. 请求域名：/Sentence/count
2. 输入参数：

```json
{
    "referer": string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Get sentence num success!", 
    "code": 0, 
    "data": 
    {
        "doing_num":doing_num,
        "done_num":done_num
    }
}
```

4. 错误码

   | Error            | Code | Description                        |
   | ---------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE   | 998  | This api only support post method! |
   | DATABASE_ERROR   | 3    | Count sentence failed              |
   | WRONG_PARAM_CODE | 2    | Input a invalid referer            |

### 5. sentence_get

1. 请求域名：/Sentence/Get
2. 输入参数：

```json
{
    "referer": string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Get a sentence success!", 
    "code": 0, 
    "data": [
        {
            "id": int,
            "content": string,
            "source": char,
            "entity_tag": bool,
            "relation_tag": bool
        }
    ]
}
```

4. 错误码

   | Error            | Code | Description                        |
   | ---------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE   | 998  | This api only support post method! |
   | DATABASE_ERROR   | 3    | Get a sentence failed              |
   | WRONG_PARAM_CODE | 2    | Input a invalid referer            |


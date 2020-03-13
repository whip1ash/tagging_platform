# Entity 接口列表

### 1. save
1. 请求域名：/entity/Save/
2. 输入参数：
```json
{
    "tag_id":int,
    "sentence_id":int,
    "pos":"x(int),y(int)",
    "entity":"Person",
    "type":int
}
```
3. 输出参数：
```json
{
    "success": true, 
    "msg": "Save Successed!", 
    "code": 0, 
    "data": ""
}
```
4. 错误码

    | Error                 | Code | Description                        |
    | --------------------- | ---- | ---------------------------------- |
    | GET_ERROR_CODE        | 998  | This api only support post method! |
    | WRONG_PARAM_CODE      | 2    | Wrong parameter[pos]               |
    | RECORD_NOT_EXIST_CODE | 404  | Wrong tag_id                       |
    | SAVE_FAILED_CODE      | 1    | Save failed!                       |

### 2. list_all

1. 请求域名：/entity/List
2. 输入参数：

```json
{
    "page": int,
	"limit": int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "", 
    "code": 0, 
    "data": [
    	{
        	"id": int,
        	"pos": "x(int),y(int)",
        	"entity": int,
        	"sentence_id": int,
        	"type_id": int
        }
    ]
}
```

4. 错误码

   | Error           | Code | Description                       |
   | --------------- | ---- | --------------------------------- |
   | DATABASE_ERROR  | 3    | List all entity tags failed !     |
   | POST_ERROR_CODE | 999  | This api only support get method! |

### 3. count

1. 请求域名：/entity/Count
2. 输入参数：

```json
{
    
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "", 
    "code": 0, 
    "data": {"count": int}
}
```

4. 错误码

   | Error           | Code | Description                       |
   | --------------- | ---- | --------------------------------- |
   | DATABASE_ERROR  | 3    | Get entity tag count failed!      |
   | POST_ERROR_CODE | 999  | This api only support get method! |

### 4. delete

1. 请求域名：/entity/Del
2. 输入参数：

```json
{
    "id":int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Delete tag success!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error                 | Code | Description                          |
   | --------------------- | ---- | ------------------------------------ |
   | DATABASE_ERROR        | 3    | This tag does't have relate sentence |
   | RECORD_NOT_EXIST_CODE | 404  |                                      |
   | GET_ERROR_CODE        | 998  | This api only support post method!   |

### 5. get

1. 请求域名：/entity/Get
2. 输入参数：

```json
{
    "id":int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Get tag success!", 
    "code": 0, 
    "data": [
    	{
        	"id": int,
        	"pos": "x(int),y(int)",
        	"entity": int,
        	"sentence_id": int,
        	"type_id": int
        }
    ]
}
```

4. 错误码

   | Error          | Code | Description                         |
   | -------------- | ---- | ----------------------------------- |
   | DATABASE_ERROR | 3    | Failed to get a entity type record. |
   | GET_ERROR_CODE | 998  | This api only support post method!  |

### 6. list_entity_type

1. 请求域名：/entity/ListType
2. 输入参数：

```json
{
    
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "", 
    "code": 0, 
    "data": [
        {
            "id": int,
            "name": string
        }
    ]
}
```

4. 错误码

   | Error          | Code | Description                        |
   | -------------- | ---- | ---------------------------------- |
   | DATABASE_ERROR | 3    | List entity type failed!           |
   | GET_ERROR_CODE | 998  | This api only support post method! |

### 7. add_entity_type

1. 请求域名：/entity/AddType
2. 输入参数：

```json
{
    "type": string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Save Successed!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error          | Code | Description                        |
   | -------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE | 998  | This api only support post method! |
   | DATABASE_ERROR | 3    | Add entity type failed!            |

### 8. del_entity_type

1. 请求域名：/entity/DelType
2. 输入参数：

```json
{
    "id":int,
    "type":string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Delete entity type success!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error                 | Code | Description                           |
   | --------------------- | ---- | ------------------------------------- |
   | GET_ERROR_CODE        | 998  | This api only support post method!    |
   | DATABASE_ERROR        | 3    | Get tags by type failed!              |
   | DELETE_ERROR          | 4    | Delete entity type failed!            |
   | RECORD_NOT_EXIST_CODE | 404  | A wrong tag id                        |
   | RECORD_NOT_EXIST_CODE | 404  | This tag doesn't have relate sentence |

### 9. edit_entity_type

1. 请求域名：/entity/EditType
2. 输入参数：

```json
{
    "id":int,
    "type":string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Edit entity type success!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error            | Code | Description                        |
   | ---------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE   | 998  | This api only support post method! |
   | SAVE_FAILED_CODE | 1    | Save failed!                       |

# Relation 接口列表

### 1. save

1. 请求域名：/relation/Save
2. 输入参数：

```json
{
    "tag_id":int,
    "sentence_id":int,
    "head_entity_pos":"x(int),y(int)",
    "head_entity":string,
    "tail_entity_pos":"x(int),y(int)",
    "tail_entity":string,
    "type_id":int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Save Successed!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error                 | Code | Description                        |
   | --------------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE        | 998  | This api only support post method! |
   | WRONG_PARAM_CODE      | 2    | Wrong parameter[pos]               |
   | RECORD_NOT_EXIST_CODE | 404  | Wrong tag_id                       |
   | SAVE_FAILED_CODE      | 1    | Save failed!                       |

### 2. list_all

1. 请求域名：/relation/List
2. 输入参数：

```json
{
    "page": int,
	"limit": int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "", 
    "code": 0, 
    "data": [
    	{
    		"tag_id":int,
    		"sentence_id":int,
    		"head_entity_pos":"x(int),y(int)",
    		"head_entity":string,
    		"tail_entity_pos":"x(int),y(int)",
    		"tail_entity":string,
    		"type_id":int
		}
    ]
}
```

4. 错误码

   | Error           | Code | Description                       |
   | --------------- | ---- | --------------------------------- |
   | DATABASE_ERROR  | 3    | List all relation tags failed !   |
   | POST_ERROR_CODE | 999  | This api only support get method! |

### 3. count

1. 请求域名：/relation/Count
2. 输入参数：

```json
{
    
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "", 
    "code": 0, 
    "data": {"count": int}
}
```

4. 错误码

   | Error           | Code | Description                       |
   | --------------- | ---- | --------------------------------- |
   | DATABASE_ERROR  | 3    | Get relation tag count failed!    |
   | POST_ERROR_CODE | 999  | This api only support get method! |

### 4. delete

1. 请求域名：/relation/Del
2. 输入参数：

```json
{
    "id":int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Delete tag success!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error                 | Code | Description                          |
   | --------------------- | ---- | ------------------------------------ |
   | DATABASE_ERROR        | 3    | This tag does't have relate sentence |
   | RECORD_NOT_EXIST_CODE | 404  |                                      |
   | GET_ERROR_CODE        | 998  | This api only support post method!   |

### 5. get

1. 请求域名：/relation/Get
2. 输入参数：

```json
{
    "id":int
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Get tag success!", 
    "code": 0, 
    "data": [
    	{
    		"tag_id":int,
    		"sentence_id":int,
    		"head_entity_pos":"x(int),y(int)",
    		"head_entity":string,
    		"tail_entity_pos":"x(int),y(int)",
    		"tail_entity":string,
    		"type_id":int
		}
    ]
}
```

4. 错误码

   | Error          | Code | Description                           |
   | -------------- | ---- | ------------------------------------- |
   | DATABASE_ERROR | 3    | Failed to get a relation type record. |
   | GET_ERROR_CODE | 998  | This api only support post method!    |

### 6. list_relation_type

1. 请求域名：/relation/ListType
2. 输入参数：

```json
{
    
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "", 
    "code": 0, 
    "data": [
        {
            "id": int,
            "name": string
        }
    ]
}
```

4. 错误码

   | Error | Code | Description |
   | ----- | ---- | ----------- |
   |       |      |             |

### 7. add_entity_type

1. 请求域名：/relation/AddType
2. 输入参数：

```json
{
    "type": string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Save Successed!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error          | Code | Description                        |
   | -------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE | 998  | This api only support post method! |
   | DATABASE_ERROR | 3    | Add realation type failed!         |

### 8. del_entity_type

1. 请求域名：/relation/DelType
2. 输入参数：

```json
{
    "id":int,
    "type":string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Delete relation type success!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error                 | Code | Description                           |
   | --------------------- | ---- | ------------------------------------- |
   | GET_ERROR_CODE        | 998  | This api only support post method!    |
   | DATABASE_ERROR        | 3    | Get tags by type failed!              |
   | DELETE_ERROR          | 4    | Delete ralation type failed!          |
   | RECORD_NOT_EXIST_CODE | 404  | A wrong tag id                        |
   | RECORD_NOT_EXIST_CODE | 404  | This tag doesn't have relate sentence |

### 9. edit_entity_type

1. 请求域名：/realtion/EditType
2. 输入参数：

```json
{
    "id":int,
    "type":string
}
```

3. 输出参数：

```json
{
    "success": true, 
    "msg": "Edit entity type success!", 
    "code": 0, 
    "data": ""
}
```

4. 错误码

   | Error            | Code | Description                        |
   | ---------------- | ---- | ---------------------------------- |
   | GET_ERROR_CODE   | 998  | This api only support post method! |
   | SAVE_FAILED_CODE | 1    | Save failed!                       |

### 
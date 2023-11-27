Aqcuire certificate token:
```
curl -X POST -H "Content-Type: application/json" -d '{"devicetype":"my_application"}' http://10.0.0.100:80/api
```

Status of all lamps:
```
curl http://10.0.0.100:80/api/token/lights
```

Toggle a Light:
```
curl -X PUT -H "Content-Type: application/json" -d '{"on":true}' http://10.0.0.109:80/api/token/lights/[LIGHT_ID]/state
```

Change Light Brightness (0-254):
```
curl -X PUT -H "Content-Type: application/json" -d '{"bri":200}' http://10.0.0.100:80/api/token/lights/[LIGHT_ID]/state
```

Rename a Light:
```
curl -X PUT -H "Content-Type: application/json" -d '{"name":"New Light Name"}' http://10.0.0.100:80/api/token/lights/[LIGHT_ID]
```

--------------------------------------------------------------------------------

Colour change:

1. **Green**:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"on":true, "hue":21845, "sat":254}' http://10.0.0.109:80/api/token/groups/1/action
   ```

2. **Purple**:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"on":true, "hue":54612, "sat":254}' http://10.0.0.109:80/api/token/groups/1/action
   ```

3. **Yellow**:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"on":true, "hue":12750, "sat":254}' http://10.0.0.109:80/api/token/groups/1/action
   ```

4. **Red**:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"on":true, "hue":0, "sat":254}' http://10.0.0.109:80/api/token/groups/1/action
   ```

5. **Pink**:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"on":true, "hue":56100, "sat":254}' http://10.0.0.109:80/api/token/groups/1/action
   ```
   
6. **Blue**:
   ```bash
   curl -X PUT -H "Content-Type: application/json" -d '{"on":true, "hue":43690, "sat":254}' http://10.0.0.109:80/api/token/groups/1/action
   ```

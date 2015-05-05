'''
Created on Apr 28, 2015

@author: mucx
'''
import Renderer
import svgwrite

#path = ('<path d="M 100 50 L 100 200 250 200 250 50 Z M 150 100 L 200 100 200 150 150 150 Z"/>)')

path_d = """M 237 200 L 239 188 243 186 242 182 243 180 265 185 270 187 
272 190 269 192 267 197 239 201 Z M 249 190 L 252 192 255 189 254 186 250 187 Z
 M 274 189 L 283 185 290 186 292 181 295 180 296 175 301 176 301 181 303 181 306 
 181 310 176 312 179 310 182 309 187 298 187 295 192 285 192 283 190 280 192 275
  191 Z"""
  
path_d = ("M 100 50 L 100 200 250 200 250 50 Z " +
    "M 150 100 L 200 100 200 150 150 150 Z")

path_d = """M -289 351 L -283 329 -279 325 -280 316 -277 303 -269 304 -267 302 -262 301 -257 296 -259 290 -258 289 -250 289 -248 292 -230 296 -230 290 -250 287 -251 285 -251 280 -247 277 -248 268 -240 259 -236 259 -235 258 -235 253 -232 250 -214 241 -211 242 -212 270 -216 271 -217 281 -215 285 -212 286 -210 284 -207 284 -198 292 -196 307 -202 314 -209 313 -210 316 -199 322 -172 309 -171 307 -156 299 -164 239 -163 233 -149 216 -132 216 -123 219 -121 219 -120 215 -92 209 -77 198 -74 198 -71 196 -71 192 -63 175 -56 169 -46 165 -40 165 -38 161 -31 159 -28 162 -33 166 -32 168 -25 169 -24 164 -20 162 -20 158 -11 158 1 162 -3 170 -7 173 -12 179 -20 176 -25 178 -25 181 -23 185 -25 190 -24 192 -32 203 -34 211 -38 218 -32 223 -33 232 -27 247 -27 249 -29 250 -33 248 -34 250 -33 258 -39 269 -43 269 -48 271 -48 274 -44 277 -47 282 -61 275 -61 270 -68 267 -76 282 -96 273 -99 276 -102 274 -99 266 -110 262 -112 260 -112 255 -120 254 -125 260 -123 265 -110 266 -110 268 -114 270 -114 273 -108 274 -108 277 -113 285 -112 287 -92 294 -85 293 -83 297 -73 302 -76 306 -80 306 -87 318 -80 324 -115 368 -129 389 -131 389 -136 379 -140 379 -143 377 -156 385 -158 390 -152 392 -152 395 -156 396 -158 391 -164 390 -170 391 -180 401 -184 400 -195 409 -197 415 -199 415 -201 411 -204 411 -207 419 -213 420 -215 417 -217 417 -219 420 -232 421 -234 416 -238 417 -239 422 -243 423 -247 419 -247 414 -249 410 -248 403 -238 406 -235 403 -229 404 -228 409 -226 410 -221 401 -215 397 -214 395 -223 383 -222 377 -222 370 -247 352 -256 358 -260 358 -264 356 -265 350 -269 348 -275 349 -282 352 -288 352 Z M -89 262 L -87 264 -83 264 -79 263 -78 260 -87 258 Z M -232 276 L -233 278 -232 280 -227 280 -227 276 -229 275 Z M -241 275 L -240 277 -234 278 -233 277 -233 272 -239 270 Z M -137 396 L -137 392 -132 393 -134 397 Z"""

#path_d = ("M 50 50 L 40 160 140 150 140 100 100 110 100 60 Z")
print (path_d)
path = svgwrite.path.Path(path_d)
print path.tostring()

svg_renderer = Renderer.Renderer()
hachure = svg_renderer.createPolygonHachure(path)

print "hachure = '" + hachure + "'"
hachure = svgwrite.path.Path(hachure)
print hachure.tostring()
# SQL framework
*SQL databases general tool*

Características de esta Plantilla Completa:
1. Métodos con Parámetros Específicos:
find(): Todos los campos como parámetros opcionales
find_many(): Incluye limit/offset + campos específicos
create(): Solo campos no autoincrementales ni primary key
update(): Filters + campos específicos para actualizar
delete(): Todos los campos como filtros específicos
2. Métodos con Flexibilidad (Diccionarios):
create_many(): Para operaciones batch
update_many(): Para actualizaciones masivas
upsert() y upsert_many(): Para operaciones complejas
3. Métodos de Conveniencia:
find_by_id(): Búsqueda rápida por ID
delete_by_id(): Eliminación rápida por ID
count(): Contar registros con filtros específicos
exists(): Verificar existencia con filtros específicos
4. Mejoras Técnicas:
Usa record_copy en update_many para no modificar los datos originales
Implementación más robusta de upsert sin usar el método update interno
Manejo correcto de primary keys dinámicas
Documentación completa para cada método
Esta plantilla proporciona el mejor balance entre type safety, flexibilidad y usabilidad para los usuarios finales del framework.
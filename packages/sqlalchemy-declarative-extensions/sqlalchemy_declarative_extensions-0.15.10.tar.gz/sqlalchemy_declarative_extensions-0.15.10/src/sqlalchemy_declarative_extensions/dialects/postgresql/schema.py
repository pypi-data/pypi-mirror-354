from sqlalchemy import (
    String,
    and_,
    bindparam,
    column,
    func,
    literal,
    table,
    text,
    union,
)
from sqlalchemy.dialects.postgresql import ARRAY, CHAR

from sqlalchemy_declarative_extensions.sqlalchemy import select

char = CHAR(1)


tables = table(
    "tables",
    column("table_schema"),
    column("table_name"),
    schema="information_schema",
)

pg_class = table(
    "pg_class",
    column("oid"),
    column("relname"),
    column("relnamespace"),
    column("relacl"),
    column("relkind", char),
    column("relowner"),
)

pg_database = table(
    "pg_database",
    column("oid"),
    column("datname"),
)

pg_namespace = table(
    "pg_namespace",
    column("oid"),
    column("nspname"),
    column("nspowner"),
    column("nspacl"),
)

pg_roles = table(
    "pg_roles",
    column("oid"),
    column("rolname"),
)

pg_default_acl = table(
    "pg_default_acl",
    column("defaclrole"),
    column("defaclnamespace"),
    column("defaclobjtype"),
    column("defaclacl"),
)

pg_views = table(
    "pg_views",
    column("schemaname"),
    column("viewname"),
    column("definition"),
)

pg_matviews = table(
    "pg_matviews",
    column("schemaname"),
    column("matviewname"),
    column("definition"),
)

pg_proc = table(
    "pg_proc",
    column("oid"),
    column("proname"),
    column("prosrc"),
    column("pronamespace"),
    column("prolang"),
    column("prorettype"),
    column("prosecdef"),
    column("prokind"),
)

pg_language = table(
    "pg_language",
    column("oid"),
    column("lanname"),
)

pg_trigger = table(
    "pg_trigger",
    column("oid"),
    column("tgname"),
    column("tgtype"),
    column("tgrelid"),
    column("tgfoid"),
    column("tgargs"),
    column("tgqual"),
    column("tgisinternal"),
)

pg_type = table(
    "pg_type",
    column("oid"),
    column("typname"),
)


roles_query = text(
    """
    SELECT
      r.rolname,
      r.rolsuper,
      r.rolinherit,
      r.rolcreaterole,
      r.rolcreatedb,
      r.rolcanlogin,
      r.rolconnlimit,
      CASE
        WHEN r.rolvaliduntil = 'infinity' THEN NULL
        ELSE r.rolvaliduntil
      END,
      ARRAY(SELECT b.rolname
            FROM pg_catalog.pg_auth_members m
            JOIN pg_catalog.pg_roles b ON (m.roleid = b.oid)
            WHERE m.member = r.oid) as memberof,
      r.rolreplication,
      r.rolbypassrls
    FROM pg_catalog.pg_roles r
    WHERE r.rolname !~ '^pg_'
    ORDER BY 1;
    """
)


def _schema_not_pg(column=pg_namespace.c.nspname):
    return and_(
        column != "information_schema",
        column.notlike("pg_%"),
    )


_schema_not_public = pg_namespace.c.nspname != "public"
_table_not_pg = pg_class.c.relname.notlike("pg_%")

schemas_query = (
    select(pg_namespace.c.nspname).where(_schema_not_pg()).where(_schema_not_public)
)


databases_query = (
    select(pg_database.c.datname)
    .where(pg_database.c.datname.notin_(["template0", "template1"]))
    .where(_schema_not_public)
)

schema_exists_query = text(
    "SELECT schema_name FROM information_schema.schemata WHERE schema_name = :schema"
)


default_acl_query = select(
    pg_roles.c.rolname.label("role_name"),
    pg_namespace.c.nspname.label("schema_name"),
    pg_default_acl.c.defaclobjtype.label("object_type"),
    pg_default_acl.c.defaclacl.cast(ARRAY(String)).label("acl"),
).select_from(
    pg_default_acl.join(pg_roles, pg_default_acl.c.defaclrole == pg_roles.c.oid).join(
        pg_namespace, pg_default_acl.c.defaclnamespace == pg_namespace.c.oid
    )
)

object_acl_query = union(
    select(
        pg_namespace.c.nspname.label("schema"),
        pg_class.c.relname.label("name"),
        pg_class.c.relkind.cast(char).label("relkind"),
        pg_roles.c.rolname.label("owner"),
        pg_class.c.relacl.cast(ARRAY(String)).label("acl"),
    )
    .select_from(
        pg_class.join(pg_namespace, pg_class.c.relnamespace == pg_namespace.c.oid).join(
            pg_roles, pg_class.c.relowner == pg_roles.c.oid
        )
    )
    .where(
        pg_class.c.relkind.cast(char).in_(
            [
                literal("r", char),
                literal("S", char),
                literal("f", char),
                literal("n", char),
                literal("T", char),
                literal("v", char),
            ]
        )
    )
    .where(_table_not_pg)
    .where(_schema_not_pg()),
    select(
        literal(None).label("schema"),
        pg_namespace.c.nspname.label("name"),
        literal("n").cast(char).label("relkind"),
        pg_roles.c.rolname.label("owner"),
        pg_namespace.c.nspacl.cast(ARRAY(String)),
    )
    .select_from(pg_namespace.join(pg_roles, pg_namespace.c.nspowner == pg_roles.c.oid))
    .where(_schema_not_pg())
    .where(_schema_not_public),
)

objects_query = (
    select(
        pg_namespace.c.nspname.label("schema"),
        pg_class.c.relname.label("object_name"),
        pg_class.c.relkind.cast(char).label("relkind"),
    )
    .select_from(
        pg_class.join(pg_namespace, pg_class.c.relnamespace == pg_namespace.c.oid)
    )
    .where(
        pg_class.c.relkind.cast(char).in_(
            [
                literal("r", char),
                literal("S", char),
                literal("f", char),
                literal("n", char),
                literal("T", char),
                literal("v", char),
            ]
        )
    )
    .where(_table_not_pg)
    .where(_schema_not_pg())
)

views_query = union(
    select(
        pg_views.c.schemaname.label("schema"),
        pg_views.c.viewname.label("name"),
        pg_views.c.definition.label("definition"),
        literal(False).label("materialized"),
    )
    .where(_schema_not_pg(pg_views.c.schemaname))
    .where(pg_views.c.viewname.notin_(["pg_stat_statements"])),
    select(
        pg_matviews.c.schemaname.label("schema"),
        pg_matviews.c.matviewname.label("name"),
        pg_matviews.c.definition.label("definition"),
        literal(True).label("materialized"),
    ).where(_schema_not_pg(pg_matviews.c.schemaname)),
)


views_subquery = views_query.cte()
view_query = (
    select(views_subquery)
    .where(views_subquery.c.schema == bindparam("schema"))
    .where(views_subquery.c.name == bindparam("name"))
)


procedures_query = (
    select(
        pg_proc.c.proname.label("name"),
        pg_namespace.c.nspname.label("schema"),
        pg_language.c.lanname.label("language"),
        pg_type.c.typname.label("return_type"),
        pg_proc.c.prosrc.label("source"),
        pg_proc.c.prosecdef.label("security_definer"),
        pg_proc.c.prokind.label("kind"),
    )
    .select_from(
        pg_proc.join(pg_namespace, pg_proc.c.pronamespace == pg_namespace.c.oid)
        .join(pg_language, pg_proc.c.prolang == pg_language.c.oid)
        .join(pg_type, pg_proc.c.prorettype == pg_type.c.oid)
    )
    .where(pg_namespace.c.nspname.notin_(["pg_catalog", "information_schema"]))
    .where(pg_proc.c.prokind == "p")
)

functions_query = (
    select(
        pg_proc.c.proname.label("name"),
        pg_namespace.c.nspname.label("schema"),
        pg_language.c.lanname.label("language"),
        pg_type.c.typname.label("return_type"),
        pg_proc.c.prosrc.label("source"),
        pg_proc.c.prosecdef.label("security_definer"),
        pg_proc.c.prokind.label("kind"),
    )
    .select_from(
        pg_proc.join(pg_namespace, pg_proc.c.pronamespace == pg_namespace.c.oid)
        .join(pg_language, pg_proc.c.prolang == pg_language.c.oid)
        .join(pg_type, pg_proc.c.prorettype == pg_type.c.oid)
    )
    .where(pg_namespace.c.nspname.notin_(["pg_catalog", "information_schema"]))
    .where(pg_proc.c.prokind != "p")
)


rel_nsp = pg_namespace.alias("rel_nsp")
proc_nsp = pg_namespace.alias("proc_nsp")
triggers_query = (
    select(
        pg_trigger.c.tgname.label("name"),
        pg_trigger.c.tgtype.label("type"),
        func.regexp_match(
            func.pg_get_triggerdef(pg_trigger.c.oid),
            literal(r" WHEN \((.+)\) EXECUTE "),
            type_=ARRAY(String),
        )[1].label("when"),
        func.string_to_array(  # split arguments by \000
            func.encode(  # convert from hex to string, \x00 to \000
                func.btrim(pg_trigger.c.tgargs, b"\x00"),  # trim trailing \x00
                "escape",
            ),
            "\\000",
        ).label("args"),
        pg_class.c.relname.label("on_name"),
        rel_nsp.c.nspname.label("on_schema"),
        pg_proc.c.proname.label("execute_name"),
        proc_nsp.c.nspname.label("execute_schema"),
    )
    .select_from(
        pg_trigger.join(pg_class, pg_trigger.c.tgrelid == pg_class.c.oid)
        .join(rel_nsp, pg_class.c.relnamespace == rel_nsp.c.oid)
        .join(pg_proc, pg_trigger.c.tgfoid == pg_proc.c.oid)
        .join(proc_nsp, pg_proc.c.pronamespace == proc_nsp.c.oid)
    )
    .where(pg_trigger.c.tgisinternal.is_(False))
)

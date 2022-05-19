"""primera migracion

Revision ID: 6ca988b5a5f9
Revises: 4ff035eafe6f
Create Date: 2022-05-18 10:51:10.495570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ca988b5a5f9'
down_revision = '4ff035eafe6f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_categorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('categoria', sa.String(), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tbl_categorias_id'), 'tbl_categorias', ['id'], unique=False)
    op.create_table('tbl_libros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_categoria', sa.Integer(), nullable=True),
    sa.Column('titulo', sa.String(), nullable=True),
    sa.Column('subtitulo', sa.String(), nullable=True),
    sa.Column('autor', sa.String(), nullable=True),
    sa.Column('fecha_publicacion', sa.DateTime(), nullable=True),
    sa.Column('editor', sa.String(), nullable=True),
    sa.Column('descripcion', sa.String(), nullable=True),
    sa.Column('disponible', sa.Boolean(), nullable=True),
    sa.Column('url_imagen', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_categoria'], ['tbl_categorias.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tbl_libros_id'), 'tbl_libros', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tbl_libros_id'), table_name='tbl_libros')
    op.drop_table('tbl_libros')
    op.drop_index(op.f('ix_tbl_categorias_id'), table_name='tbl_categorias')
    op.drop_table('tbl_categorias')
    # ### end Alembic commands ###
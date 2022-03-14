# Generated by Django 2.2.5 on 2022-03-11 17:47

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Constraint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='No description')),
                ('labels', models.CharField(blank=True, default='', max_length=100)),
                ('type', models.CharField(choices=[('scalar', 'Scalar'), ('array', 'Array'), ('hashmap', 'Hashmap'), ('unknown', 'Unknown')], default='unknown', max_length=100)),
                ('shape', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='No description')),
                ('labels', models.CharField(blank=True, default='', max_length=100)),
                ('type', models.CharField(choices=[('scalar', 'Scalar'), ('array', 'Array'), ('hashmap', 'Hashmap'), ('unknown', 'Unknown')], default='unknown', max_length=100)),
                ('shape', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('objective', models.CharField(choices=[('scalar', 'Scalar'), ('array', 'Array'), ('hashmap', 'Hashmap'), ('unknown', 'Unknown')], default='unknown', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='New Model', max_length=100)),
                ('description', models.TextField(default='No description')),
                ('system', models.CharField(choices=[('optmod', 'Optmod'), ('jump', 'JuMP'), ('cvxpy', 'CVXPY'), ('gams', 'GAMS'), ('pyomo', 'Pyomo')], max_length=100)),
                ('status', models.CharField(choices=[('created', 'Created'), ('running', 'Running'), ('success', 'Success'), ('unknown', 'Unknown'), ('error', 'Error')], default='created', max_length=100)),
                ('source', models.TextField(default='')),
                ('time_created', models.DateTimeField()),
                ('time_start', models.DateTimeField(default=None, null=True)),
                ('time_end', models.DateTimeField(default=None, null=True)),
                ('execution_log', models.TextField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='models', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='problem', to='backend.Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problems', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Solver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('model', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='solver', to='backend.Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solvers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='No description')),
                ('labels', models.CharField(blank=True, default='', max_length=100)),
                ('type', models.CharField(choices=[('scalar', 'Scalar'), ('array', 'Array'), ('hashmap', 'Hashmap'), ('unknown', 'Unknown')], default='unknown', max_length=100)),
                ('shape', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables', to='backend.Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variables', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VariableState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('label', models.CharField(blank=True, default='', max_length=200)),
                ('kind', models.CharField(choices=[('continuous', 'Continuous'), ('integer', 'Integer'), ('binary', 'Binary'), ('unknown', 'Unknown')], default='unknown', max_length=100)),
                ('value', models.FloatField(default=0.0)),
                ('upper_bound', models.FloatField(default=0.0)),
                ('lower_bound', models.FloatField(default=0.0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_states', to=settings.AUTH_USER_MODEL)),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='backend.Variable')),
            ],
        ),
        migrations.CreateModel(
            name='SolverState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('message', models.TextField(blank=True, default='')),
                ('iterations', models.IntegerField(default=0)),
                ('time', models.FloatField(default=0.0)),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solver_states', to=settings.AUTH_USER_MODEL)),
                ('solver', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='backend.Solver')),
            ],
        ),
        migrations.CreateModel(
            name='ProblemState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(choices=[('lp', 'Lp'), ('nlp', 'Nlp'), ('milp', 'Milp'), ('convex', 'Convex'), ('mip', 'mip'), ('mcp', 'mcp'), ('unknown', 'Unknown')], default='unknown', max_length=100)),
                ('num_vars', models.IntegerField(default=0)),
                ('num_constraints', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problem_states', to=settings.AUTH_USER_MODEL)),
                ('problem', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='backend.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='InterfaceObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='No description')),
                ('type', models.CharField(choices=[('input', 'Input'), ('output', 'Output')], max_length=100)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('data_size', models.IntegerField(default=0)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interface_objects', to='backend.Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interface_objects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InterfaceFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, default='No description')),
                ('filename', models.CharField(blank=True, default='', max_length=100)),
                ('type', models.CharField(choices=[('input', 'Input'), ('output', 'Output')], max_length=100)),
                ('extension', models.CharField(blank=True, default='', max_length=100)),
                ('data', models.FileField(blank=True, null=True, upload_to='')),
                ('data_size', models.IntegerField(default=0)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interface_files', to='backend.Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interface_files', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HelperObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='No description')),
                ('type', models.CharField(choices=[('pre', 'Pre-optimization'), ('post', 'Post-optimization')], max_length=100)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('data_size', models.IntegerField(default=0)),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helper_objects', to='backend.Model')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helper_objects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FunctionState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('label', models.CharField(blank=True, default='', max_length=200)),
                ('value', models.FloatField(default=0.0)),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='backend.Function')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_states', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='function',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='functions', to='backend.Model'),
        ),
        migrations.AddField(
            model_name='function',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='functions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ConstraintState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('label', models.CharField(blank=True, default='', max_length=200)),
                ('kind', models.CharField(choices=[('equality', 'Equality'), ('inequality', 'Inequality'), ('unknown', 'Unknown')], max_length=100)),
                ('dual', models.FloatField(default=0.0)),
                ('violation', models.FloatField(default=0.0)),
                ('constraint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='backend.Constraint')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='constraint_states', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='constraint',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='constraints', to='backend.Model'),
        ),
        migrations.AddField(
            model_name='constraint',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='constraints', to=settings.AUTH_USER_MODEL),
        ),
    ]

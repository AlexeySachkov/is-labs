%������:
%���������� � ����������� ������� ��������� ����������
%�������� �� ������ ����������� ������ � ������ ��������.
%���� ������ 4 � 5 - �������� +25%, ��� 5 - 50%

%�������� ������:
%-������, �������, ���, �������� ��������, ����� �������� ������, ����� �������� (������/���������)
%-����� �������� ������, ������ �� ���� ���������

%���������:
%����� �������� ������, ���������� ��������� (��/���), � ������

%������� �� Visual Prolog 5.2
PREDICATES
nondeterm �������(symbol, symbol, symbol, symbol, integer, symbol).
nondeterm �������(integer, integer, integer, integer, integer, integer).
�������_���������(real).
nondeterm ����������(integer, symbol).
nondeterm ��������_0(integer).
nondeterm ��������_25(integer).
nondeterm ��������_50(integer).
nondeterm ������(integer, real).
nondeterm �����������_���������(integer,symbol,real).
nondeterm ���_�����(integer)
CLAUSES
�������(��16��, ������, ����, ��������, 161130, ������).%�1
�������(��15���, ������, ����, ��������, 197412, ������).%�2
�������(��15���, ��������, �������, ����������, 139754, ���������).%�3
�������(��15���, ��������, ������, ����������, 132846, ������).%�4
�������(��15��, �����������, ���������, �������������, 172398, ������).%�5
�������(161130, 5, 4, 3, 5, 4).%�6
�������(197412, 5, 4, 4, 4, 4).%�7
�������(139754, 5, 5, 5, 5, 5).%�8
�������(132846, 5, 5, 5, 5, 5).%�9
�������(172398, 4, 4, 4, 4, 4).%�10
�������_���������(2500).%�11
���_�����(�������):-�������(�������,�1,�2,�3,�4,�5),�1>3,�2>3,�3>3,�4>3,�5>3.%��1
����������(�������,����������):-�������(_,_,_,_,�������,������),���_�����(�������),����������=��.%��2
����������(�������,����������):-�������(_,_,_,_,�������,������),not(���_�����(�������)),����������=���.%��3
����������(�������,����������):-�������(_,_,_,_,�������,���������),����������=���.%��4
��������_0(�������):-�������(�������,4,4,4,4,4).%��5
��������_50(�������):-�������(�������,5,5,5,5,5).%��6
��������_25(�������):-���_�����(�������),not(��������_0(�������)),not(��������_50(�������)).%��7
������(�������,������):-����������(�������,���),������=0.%��8
������(�������,������):-����������(�������,��),��������_0(�������),�������_���������(������).%��9
������(�������,������):-����������(�������,��),��������_25(�������),�������_���������(�������),������=�������*1.25.%��10
������(�������,������):-����������(�������,��),��������_50(�������),�������_���������(�������),������=�������*1.5.%��11
�����������_���������(�������,����������,������):-����������(�������,����������),������(�������,������).%��12
GOAL
�����������_���������(�������,����������,������),�������(������,�������,���,��������,�������,_).%�1

%OUTPUT:
%�������=197412, ����������=��, ������=3125, ������=��15���, �������=������, ���=����, ��������=��������
%�������=132846, ����������=��, ������=3750, ������=��15���, �������=��������, ���=������, ��������=����������
%�������=172398, ����������=��, ������=2500, ������=��15��, �������=�����������, ���=���������, ��������=�������������
%�������=161130, ����������=���, ������=0, ������=��16��, �������=������, ���=����, ��������=��������
%�������=139754, ����������=���, ������=0, ������=��15���, �������=��������, ���=�������, ��������=����������
%5 Solutions
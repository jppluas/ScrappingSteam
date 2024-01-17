import 'dart:io';
import 'package:csv/csv.dart';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Chart Example'),
        ),
        body: ChartSwitcher(),
      ),
    );
  }
}

class ChartSwitcher extends StatefulWidget {
  @override
  _ChartSwitcherState createState() => _ChartSwitcherState();
}

class _ChartSwitcherState extends State<ChartSwitcher> {
  int _selectedIndex = 0;
  List<List<dynamic>> csvData = []; // Almacena los datos leídos del archivo CSV

  @override
  void initState() {
    super.initState();
    _readCsv(); // Llamada a la función para leer el archivo CSV al inicializar el widget
  }

  Future<void> _readCsv() async {
    final File file = File(
        'ruta_del_archivo.csv'); // Reemplaza 'ruta_del_archivo.csv' con la ruta correcta de tu archivo CSV

    if (await file.exists()) {
      final List<List<dynamic>> data = await readCsv(file);
      setState(() {
        csvData = data;
      });
    } else {
      print('El archivo no existe.');
    }
  }

  Future<List<List<dynamic>>> readCsv(File file) async {
    final String content = await file.readAsString();
    final List<List<dynamic>> csvList = CsvToListConverter().convert(content);
    return csvList;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Expanded(
          child: Padding(
            padding: EdgeInsets.all(30.0),
            child: _buildChart(),
          ),
        ),
        BottomNavigationBar(
          items: [
            BottomNavigationBarItem(
              icon: Icon(Icons.bar_chart),
              label: 'Barras',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.pie_chart),
              label: 'Pastel',
            ),
            BottomNavigationBarItem(
              icon: Icon(Icons.scatter_plot),
              label: 'Dispersión',
            ),
          ],
          currentIndex: _selectedIndex,
          onTap: (index) {
            setState(() {
              _selectedIndex = index;
            });
          },
        ),
      ],
    );
  }

  Widget _buildChart() {
    switch (_selectedIndex) {
      case 0:
        return BarChartWidget();
      case 1:
        return PieChartWidget();
      case 2:
        return ScatterChartWidget();
      default:
        return Container();
    }
  }
}

class BarChartWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: BarChart(
        BarChartData(
          alignment: BarChartAlignment.center,
          barGroups: [
            BarChartGroupData(
              x: 0,
              barRods: [
                BarChartRodData(
                  y: 8,
                  colors: [Colors.blue],
                ),
              ],
            ),
            BarChartGroupData(
              x: 1,
              barRods: [
                BarChartRodData(
                  y: 12,
                  colors: [Colors.green],
                ),
              ],
            ),
            BarChartGroupData(
              x: 2,
              barRods: [
                BarChartRodData(
                  y: 5,
                  colors: [Colors.red],
                ),
              ],
            ),
          ],
          borderData: FlBorderData(show: true),
          titlesData: FlTitlesData(
            leftTitles: SideTitles(
              showTitles: true,
              interval: 5,
            ),
            rightTitles: SideTitles(
              showTitles: false,
            ),
            topTitles: SideTitles(
              showTitles: true,
              interval: 5,
            ),
            bottomTitles: SideTitles(
              showTitles: true,
              getTitles: (double value) {
                switch (value.toInt()) {
                  case 0:
                    return 'A';
                  case 1:
                    return 'B';
                  case 2:
                    return 'C';
                  default:
                    return '';
                }
              },
            ),
          ),
        ),
      ),
    );
  }
}

class PieChartWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Stack(
        children: [
          PieChart(
            PieChartData(
              sections: [
                PieChartSectionData(
                  value: 8,
                  color: Colors.blue,
                  title: 'A',
                  radius: 40,
                  titleStyle: TextStyle(color: Colors.white, fontSize: 16),
                ),
                PieChartSectionData(
                  value: 12,
                  color: Colors.green,
                  title: 'B',
                  radius: 40,
                  titleStyle: TextStyle(color: Colors.white, fontSize: 16),
                ),
                PieChartSectionData(
                  value: 5,
                  color: Colors.red,
                  title: 'C',
                  radius: 40,
                  titleStyle: TextStyle(color: Colors.white, fontSize: 16),
                ),
              ],
              borderData: FlBorderData(show: false),
              sectionsSpace: 0,
            ),
          ),
          Center(
            child: Padding(
              padding: EdgeInsets.all(30.0),
              child: Text(
                'Total',
                style: TextStyle(color: Colors.white, fontSize: 18),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class ScatterChartWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: ScatterChart(
        ScatterChartData(
          scatterSpots: [
            ScatterSpot(100000, 5, radius: 15, color: Colors.blue),
            ScatterSpot(50000, 8, radius: 20, color: Colors.green),
            ScatterSpot(100, 12, radius: 25, color: Colors.red),
          ],
          borderData: FlBorderData(show: true),
          gridData: FlGridData(show: true),
          titlesData: FlTitlesData(
            leftTitles: SideTitles(
              showTitles: true,
            ),
            rightTitles: SideTitles(
              showTitles: false,
            ),
            topTitles: SideTitles(
              showTitles: false,
            ),
            bottomTitles: SideTitles(
              showTitles: true,
            ),
          ),
        ),
      ),
    );
  }
}

package agents;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

class FruitSellerGui extends JFrame {
    private FruitSellerAgent myAgent;

    private JTextField nameField, priceField;

    FruitSellerGui(FruitSellerAgent a) {
        super(a.getLocalName());

        myAgent = a;

        JPanel p = new JPanel();
        p.setLayout(new GridLayout(2, 2));
        p.add(new JLabel("Fruit name:"));
        nameField = new JTextField(15);
        p.add(nameField);
        p.add(new JLabel("Price:"));
        priceField = new JTextField(15);
        p.add(priceField);
        getContentPane().add(p, BorderLayout.CENTER);

        JButton addButton = new JButton("Add");
        addButton.addActionListener( new ActionListener() {
            public void actionPerformed(ActionEvent ev) {
                try {
                    String name = nameField.getText().trim();
                    String price = priceField.getText().trim();
                    myAgent.updateCatalogue(name, Integer.parseInt(price));
                    nameField.setText("");
                    priceField.setText("");
                } catch (Exception e) {
                    JOptionPane.showMessageDialog(FruitSellerGui.this, "Invalid values. "+e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        } );
        p = new JPanel();
        p.add(addButton);
        getContentPane().add(p, BorderLayout.SOUTH);

        //Make the agent terminate when the user closes
        //the GUI using the button on the upper right corner
        addWindowListener(new   WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                myAgent.doDelete();
            }
        } );

        setResizable(false);
    }

    public void show() {
        pack();
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int centerX = (int)screenSize.getWidth() / 2;
        int centerY = (int)screenSize.getHeight() / 2;
        setLocation(centerX - getWidth() / 2, centerY - getHeight() / 2);
        super.show();
    }
}
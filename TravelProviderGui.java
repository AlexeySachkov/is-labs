package travelagent;
import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.GridLayout;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
class TravelProviderGui extends JFrame {
    private static final long serialVersionUID = 1L;
    private TravelProvider myAgent;
    private JTextField titleField, jbField, priceField;
    TravelProviderGui(TravelProvider a) {
        super(a.getLocalName());
        myAgent = a;
        JPanel p = new JPanel();
        p.setLayout(new GridLayout(3, 2));
        p.add(new JLabel("Destination City:"));
        titleField = new JTextField(15);
        p.add(titleField);
        p.add(new JLabel("Departure Schedule:"));
        jbField = new JTextField(15);
        p.add(jbField);
        p.add(new JLabel("Cost:"));
        priceField = new JTextField(15);
        p.add(priceField);
        getContentPane().add(p, BorderLayout.CENTER);
        JButton addButton = new JButton("Add");
        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent ev) {
                try {
                    String title = titleField.getText().trim();
                    String scheduleDepart = jbField.getText().trim();
                    String price = priceField.getText().trim();
                    String[] day = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"};
                    int jb=0;
                    for (int i = 0; i < day.length; i++) {
                        if (scheduleDepart.equals(day[i])) {
                            jb = i;
                        }
                    }
                    myAgent.updateCatalogue(title, price, jb);
                    titleField.setText("");
                    priceField.setText("");
                    jbField.setText("");
                } catch (Exception e) {
                    JOptionPane.showMessageDialog(TravelProviderGui.this, "Invalid values. " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
                }
            }
        });
        p = new JPanel();
        p.add(addButton);
        getContentPane().add(p, BorderLayout.SOUTH);

        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                myAgent.doDelete();
            }
        });
        setResizable(false);
    }
    public void showGui() {
        pack();
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int centerX = (int) screenSize.getWidth() / 2;
        int centerY = (int) screenSize.getHeight() / 2;
        setLocation(centerX - getWidth() / 2, centerY - getHeight() / 2);
        super.setVisible(true);
    }
}

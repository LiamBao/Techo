public class solution{

    /**
     *  parse XML file
     */
    File file = new File(path);
    if (!file.exists()) {
        throw new IOException("Can't find " + path);
    }

    SAXReader reader = new SAXReader();
    Document  document = reader.read(file);
    Element root = document.getRootElement();
    for (Iterator<?> i = root.elementIterator(); i.hasNext();)
    {
        Element page = (Element) i.next();
        if(page.attributeCount()>0){
            System.out.print(page.toString());
        }
    }


    /**
     * parse file path after java -jar
     */
    String base = System.getProperty("java.class.path");

        File file = null;

        if(System.getProperty("os.name").startsWith("Win")){
            if(base.endsWith(".jar")){
                base=base.substring(0, base.lastIndexOf("\\")+1);
            }

            file=new File(base+"\\properties.yml");
            path = base+"\\properties.yml";
        }else if (System.getProperty("os.name").startsWith("Mac") || System.getProperty("os.name").startsWith("Linux")){
            if(base.endsWith(".jar")){
                base=base.substring(0, base.lastIndexOf("/")+1);
            }
            /**
             *  jar
            */
           // file=new File(base+"/properties.yml");
           // path = base+"/properties.yml";

            /**
             * development environment
             */
//            file = new File("src/main/resources/config/properties.yml");
            file = new File(path);
        }else {
            System.err.println("Platform shoud be Windows/Mac/Linux");
            System.exit(1);
        }


        /**
         * 
         */


}



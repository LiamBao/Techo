#!/bin/bash
#
#In some situations i like to use INI files as configuration files,
# as python do. But bash do not provide a parser for these files, 
#obviously you can use a awk code or a couple of sed calls, 
#but if you are bash-priest and do not want to use nothing more, 
#then you can try the following obscure code


#### config file 

cat > $pathtoyourpro/configfile.ini <<EOF
; INI file  
[config_part_1]
ip=10.10.10.99
username=root

[config_part_2]
buildipaddress=10.10.10.90
buildusername=root

EOF

cfg.parser ()
{
    ini="$(<$1)"                # read the file
    ini="${ini//[/\[}"          # escape [
    ini="${ini//]/\]}"          # escape ]
    IFS=$'\n' && ini=( ${ini} ) # convert to line-array
    ini=( ${ini[*]//;*/} )      # remove comments with ;
    ini=( ${ini[*]/\    =/=} )  # remove tabs before =
    ini=( ${ini[*]/=\   /=} )   # remove tabs be =
    ini=( ${ini[*]/\ =\ /=} )   # remove anything with a space around =
    ini=( ${ini[*]/#\\[/\}$'\n'cfg.section.} ) # set section prefix
    ini=( ${ini[*]/%\\]/ \(} )    # convert text2function (1)
    ini=( ${ini[*]/=/=\( } )    # convert item to array
    ini=( ${ini[*]/%/ \)} )     # close array parenthesis
    ini=( ${ini[*]/%\\ \)/ \\} ) # the multiline trick
    ini=( ${ini[*]/%\( \)/\(\) \{} ) # convert text2function (2)
    ini=( ${ini[*]/%\} \)/\}} ) # remove extra parenthesis
    ini[0]="" # remove first element
    ini[${#ini[*]} + 1]='}'    # add the last brace
    eval "$(echo "${ini[*]}")" # eval the result
}



cfg.writer ()
{
    IFS=' '$'\n'
    fun="$(declare -F)"
    fun="${fun//declare -f/}"
    for f in $fun; do
        [ "${f#cfg.section}" == "${f}" ] && continue
        item="$(declare -f ${f})"
        item="${item##*\{}"
        item="${item%\}}"
        item="${item//=*;/}"
        vars="${item//=*/}"
        eval $f
        echo "[${f#cfg.section.}]"
        for var in $vars; do
            echo $var=\"${!var}\"
        done
    done
}


cfg.parser $conffile
# enable section called 'sec2' (in the file [sec2]) for reading

cfg.section.config_part_1
ip=$ip
username=$username

cfg.section.config_part_2
ip=
username=


# read the content of the variable called 'var2' (in the file
# var2=XXX). If your var2 is an array, then you can use
# ${var[index]}
echo "$var2"

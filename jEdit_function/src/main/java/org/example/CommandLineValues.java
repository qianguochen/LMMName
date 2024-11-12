package org.common;

import org.kohsuke.args4j.CmdLineException;
import org.kohsuke.args4j.CmdLineParser;
import org.kohsuke.args4j.Option;

/**
 * This class handles the programs arguments.
 */
public class CommandLineValues {

	@Option(name = "--dir", required = true)
	public String Dir = null;

	@Option(name = "--file", required = true)
	public String fileName = null;

	@Option(name = "--num_threads", required = true)
	public int NumThreads = 0;

	@Option(name = "--contain_content", required = false)
	public boolean isContainContent;

	public CommandLineValues(String... args) throws CmdLineException {
		CmdLineParser parser = new CmdLineParser(this);
		try {
			parser.parseArgument(args);
		} catch (CmdLineException e) {
			System.err.println(e.getMessage());
			parser.printUsage(System.err);
			throw e;
		}
	}
	public CommandLineValues() {

	}

	@Override
	public String toString() {
		final StringBuffer sb = new StringBuffer("CommandLineValues{");
		sb.append("Dir='").append(Dir).append('\'');
		sb.append(", fileName='").append(fileName).append('\'');
		sb.append(", NumThreads=").append(NumThreads);
		sb.append(", isContainContent=").append(isContainContent);
		sb.append('}');
		return sb.toString();
	}
}